import uuid
import sqlalchemy as sa
from datetime import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def make_uuid():
    '''Create a universally unique ID'''
    return str(uuid.uuid4())


class IdMixin(object):
    id = sa.Column(sa.CHAR(36), primary_key=True, default=make_uuid)


class TimestampMixin(object):
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    updated = sa.Column(sa.DateTime, onupdate=datetime.utcnow)


class Session(TimestampMixin, db.Model):
    id = sa.Column(sa.String, primary_key=True)

    messages = sa.orm.relationship('Message')


class Message(IdMixin, TimestampMixin, db.Model):
    session_id = sa.Column(sa.ForeignKey('session.id'))
    phone_number = sa.Column(sa.String(15), nullable=False)
    service_code = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=False)
    reply = sa.Column(sa.String, nullable=True)

    session = sa.orm.relationship('Session')
