import uuid
import sqlalchemy as sa
from datetime import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def make_uuid():
    '''Create a universally unique ID'''
    return str(uuid.uuid4())


class ModelMixin(object):
    id = sa.Column(sa.CHAR(36), primary_key=True, default=make_uuid)
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    updated = sa.Column(sa.DateTime, onupdate=datetime.utcnow)


class User(ModelMixin, db.Model):
    name = sa.Column(sa.String())
