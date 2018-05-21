import googlemaps
import html
import logging
import random
from datetime import datetime
from flask import current_app
from roadsafety.models import db, Session, Message, TrafficReport


def _get_logger():
    try:
        return current_app.logger
    except:
        return logging.getLogger(__name__)


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

# Google Maps Handlers


def get_direction(origin, destination):
    log = _get_logger()
    log.debug({'origin': origin, 'destination': destination})
    try:
        client = _create_googlemaps_client()
        routes = client.directions(
            origin, destination, mode='driving', alternatives=False, language='en',
            units='metric', region='ng', departure_time=datetime.utcnow(), transit_mode='bus',
            traffic_model='best_guess')

        if not len(routes):
            return 'No direction was found for the giving origin/destination.'

        log.debug({'routes': routes})
        best_route = routes[0]
        steps = []
        for leg in best_route['legs']:
            for step in leg['steps']:
                steps.append(html.unescape(step['html_instructions']))

        direction = ', '.join(steps)
        distance = best_route['distance']['text']
        duration = best_route['duration']['text']

        direction_text = '{}. (distance: {}, duration: {})'.format(
            direction, distance, duration)

        return direction_text
    except Exception as e:
        log.error(str(e))
        return 'Unable to get directions at this moment.'


def store_traffic_report(location, status, reported_by):
    report = TrafficReport(
        location=location, status=status, reported_by=reported_by
    )
    db.session.add(report)
    db.session.commit()


TRAFFIC_VIOLATIONS = [
    'LIGHT/SIGN VIOLATION|2,000',
    'ROAD OBSTRUCTION|3000',
    'ROUTE VIOLATION|5000',
    'SPEED LIMIT VIOLATION|3,000',
    'VEHICLE LICENCE VIOLATION|3,000',
    'VEHICLE NUMBER PLATE VIOLATION|3,000'
    'DRIVER\'S LICENCE VIOLATION|10,000',
    'WRONGFUL OVERTAKING|3,000',
    'ROAD MARKING VIOLATION|5,000',
    'CAUTION SIGN VIOLATION|3,000',
    'DANGEROUS DRIVING|50,000',
    'DRIVING UNDER ALCOHOL OR DRUG INFLUENCE|5,000',
    'OPERATING A VEHICLE WITH FORGED DOCUMENTS|20,000',
    'UNAUTHORIZED REMOVAL OF OR TAMPERING WITH ROAD SIGNS|5,000',
    'DO NOT MOVE VIOLATION|2,000',
    'INADEQUATE CONSTRUCTION WARNING|50,000',
    'CONSTRUCTION AREA SPEED LIMIT VIOLATION|3,000',
    'FAILURE TO MOVE OVER|3,000',
    'FAILURE TO COVER UNSTABLE MATERIALS|5,000',
    'OVERLOADING|10,000',
    'DRIVING WITH WORN­OUT TYRE OR WITHOUT SPARE TYRE|3,000',
    'DRIVING WITHOUT OR WITH SHATTERED WINDSCREEN|2,000',
    'FAILURE TO FIX RED FLAG ON PROJECTED LOAD|3,000',
    'FAILURE TO REPORT ACCIDENT|20,000',
    'MEDICAL PERSONNEL OR HOSPITAL REJECTION OF ROAD ACCIDENT VICTIM|50,000',
    'ASSAULTING MARSHAL ON DUTY|10,000',
    'OBSTRUCTING MARSHAL ON DUTY|2,000',
    'ATTEMPTING TO CORRUPT MARSHAL|10,000',
    'CUSTODY FEE for impounded vehicles is 200 naira per day after the first 24 hours',
    'DRIVING WITHOUT SPECIFIED FIRE EXTINGUISHER|3,000',
    'DRIVING A COMMERCIAL VEHICLE WITHOUT PASSENGER MANIFEST|10,000',
    'DRIVING WITHOUT SEAT BELT|2,000',
    'USE OF PHONE WHILE DRIVING|4,000',
    'RIDING MOTORCYCLE WITHOUT A CRASH HELMET|2,000',
    'DRIVING A VEHICLE WHILE UNDER 18 YEARS|2,000',
    'EXCESSIVE SMOKE EMISSION|5,000',
    'MECHANICALLY DEFICIENT VEHICLE|5,000',
    'FAILURE TO INSTALL SPEED LIMITING DEVICE|3,000'
]


def get_random_tip():
    global TRAFFIC_VIOLATIONS
    tip = random.choice(TRAFFIC_VIOLATIONS)
    if not '|' in tip:
        return tip.capitalize()

    start, end = tip.split('|')
    return ' '.join([start, 'carries a fine of', end, 'naira']).lower().capitalize()


# Welcome to TMS
# 1. Travel Planning
#   - Origin
#       - Destination
#           - Result
# 2. Report Traffic
#     Location
#       Condition
#       1:- Light Traffic
#       2:- Heavy Traffic
#       3:- Road Diversion
#       4:- Accident
#           - Result
# 3. Road Safety Tips
#   - Result


class ParseError(Exception):
    pass


def parse_and_reply(ussd):
    '''Parses the USSD message text and returns a reply text'''
    text = ussd.get('text', '').strip()
    if not text:
        raise ParseError('Empty text!')

    parts = [t.strip() for t in text.split('*')]
    if parts[0] == '1':
        # Travel Planning
        if len(parts) == 1:
            # Origin
            return 'CONOrigin:'
        elif len(parts) == 2:
            # Destination
            return 'CONDestination:'
        else:
            origin, destination = parts[1:]
            return '{}END'.format(get_direction(origin, destination))
    elif parts[0] == '2':
        # Report Traffic
        if len(parts) == 1:
            # Location
            return 'CONLocation:'
        elif len(parts) == '2':
            # Report
            return 'CONReport:'
        else:
            # store traffic report
            location, status = parts[1:]
            reported_by = ussd['phoneNumber']
            store_traffic_report(location, status, reported_by)
            return 'Thanks for ReportingEND'
    else:
        # Road safety tip
        return '{}END'.format(get_random_tip())
