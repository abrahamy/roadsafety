import functools
import requests
from authlib.flask.client import OAuth
from dotenv import load_dotenv, find_dotenv
from flask import (
    abort, Blueprint, current_app, flash, redirect,
    render_template, request, session, url_for)
from six.moves.urllib.parse import urlencode
from roadsafety.forms import SignUpForm


blueprint = Blueprint('auth', __name__, url_prefix='/auth')
auth = None


@blueprint.record_once
def init_auth(state):
    global auth

    oauth = OAuth(state.app)
    config = state.app.config
    provider = config.get('AUTH_PROVIDER')
    scope = config.get('AUTH_SCOPE')
    domain = config.get('AUTH_DOMAIN')
    client_id = config.get('AUTH_CLIENT_ID')
    client_secret = config.get('AUTH_CLIENT_SECRET')

    auth = oauth.register(
        provider,
        client_id=client_id,
        client_secret=client_secret,
        api_base_url=domain,
        access_token_url='{}/oauth/token'.format(domain),
        authorize_url='{}/authorize'.format(domain),
        client_kwargs={
            'scope': scope,
        },
    )


def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect(url_for('auth.signin'))
        return f(*args, **kwargs)

    return decorated


@blueprint.route('/callback')
def callback():
    # Handles response from token endpoint
    resp = auth.authorize_access_token()

    url = '{}/userinfo'.format(auth.api_base_url)
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect(url_for('site.dashboard'))


@blueprint.route('/signin')
def signin():
    return auth.authorize_redirect(
        redirect_uri=url_for('auth.callback'),
        audience='{}/userinfo'.format(auth.api_base_url)
    )


@blueprint.route('/logout')
@login_required
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        'returnTo': url_for('site.index', _external=True),
        'client_id': auth.client_id
    }
    logout_url = '{}/v2/logout?{}'.format(auth.api_base_url, urlencode(params))

    return redirect(logout_url)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)

    if request.method == 'POST' and form.validate():
        params = {
            'client_id': auth.api_base_url,
            'email': form.email.data,
            'password': form.password.data,
            'connection': current_app.config.get('AUTH_CONNECTION'),
            'user_metadata': {
                'name': form.name.data,
                'accept_tos': form.accept_tos.data
            }
        }

        signup_url = '{}/dbconnections/signup?{}'.format(
            auth.api_base_url, urlencode(params))

        # get access token
        resp = auth.authorize_access_token()
        headers = {'authorization': 'Bearer ' + resp['access_token']}

        # register user
        resp = requests.post(signup_url, headers=headers)
        if resp.ok:
            abort(400)

        flash('Thanks for signing up!')
        return redirect(url_for('auth.signin'))

    return render_template('auth/signup.html', form=form)
