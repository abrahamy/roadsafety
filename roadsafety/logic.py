import googlemaps
from flask import current_app
from roadsafety.models import db, Session, Message


def _create_googlemaps_client():
    return googlemaps.Client(key=current_app.config.get('GOOGLE_MAPS_KEY'))


def record(ussd, reply):
    session = Session.query.get(ussd['sessionId'])

    if not session:
        session = Session(id=ussd['sessionId'])

    message = Message(
        session_id=session.id,
        phone_number=ussd['phoneNumber'],
        service_code=ussd['serviceCode'],
        text=ussd['text'],
        reply=reply
    )

    db.session.add(session)
    db.session.add(message)
    db.session.commit()


def parse_and_reply(ussd_text):
    '''Parses the USSD message text and returns a reply text'''
    return 'just some random gibberish'
