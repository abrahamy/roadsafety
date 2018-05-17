import wtforms as forms
from wtforms import validators


class SignUpForm(forms.Form):
    name = forms.StringField('Name', [validators.DataRequired()])
    email = forms.StringField('Email Address', [
        validators.DataRequired(),
        validators.Email()
    ])
    password = forms.PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = forms.PasswordField('Repeat Password')
    accept_tos = forms.BooleanField('I accept the TOS', [
        validators.DataRequired(
            'You must accept the terms of service to sign up.')
    ])
