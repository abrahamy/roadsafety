from flask import Blueprint
from roadsafety.models import db, User
from roadsafety.blueprints.auth import login_required


blueprint = Blueprint('site', __name__, url_prefix='/')


@blueprint.route('/')
def index():
    return 'Hello, World!'


@blueprint.route('/dashboard')
@login_required
def dashboard():
    return 'Dashboard'
