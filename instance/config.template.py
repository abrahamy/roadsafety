import os


DEBUG = True
SECRET_KEY = os.getenv(
    'FLASK_SECRET_KEY', 'xW#oP&VUqvYA{mma$Fb^wTnNXCV3UndUqJ&E')

# Database
DATABASE = os.path.join(os.path.dirname(__file__), 'roadsafety.sqlite')

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE)
SQLALCHEMY_ECHO = DEBUG
# SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG

# OAuth
AUTH_PROVIDER = os.getenv('AUTH_PROVIDER', 'auth0')
AUTH_DOMAIN = os.getenv('AUTH_DOMAIN')
AUTH_SCOPE = os.getenv('AUTH_SCOPE', 'openid profile')
AUTH_CLIENT_ID = os.getenv('AUTH_CLIENT_ID')
AUTH_CLIENT_SECRET = os.getenv('AUTH_CLIENT_SECRET')
AUTH_CONNECTION = os.getenv('AUTH_CONNECTION')

# Google Maps
GOOGLE_MAPS_KEY = ""
