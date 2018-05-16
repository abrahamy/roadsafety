from flask import Blueprint
from roadsafety.models import db, User


blueprint = Blueprint('home', __name__, url_prefix='/')


@blueprint.route('/')
def index():
    return 'Hello, World!'
