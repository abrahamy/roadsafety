from flask import Blueprint
from flask_restplus import Api
from roadsafety.models import User

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
