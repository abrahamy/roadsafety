from flask import Blueprint
from flask_restplus import Api, fields, Resource
import roadsafety.logic as logic


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, description='Callback for Africa\'s Talking USSD API')
ns = api.namespace('ussd', description='Receive USSD Messages')

ussd = api.model('USSD', {
    'sessionId': fields.String(required=True, description=(
        'This is a session unique value generated when the session starts '
        'and sent every time a mobile subscriber response has been received'
    )),
    'phoneNumber': fields.String(required=True, description='This is the mobile subscriber number'),
    'serviceCode': fields.String(required=True, description=(
        'This is your USSD code. Please note that it doesn\'t '
        'show your channel for shared USSD codes.'
    )),
    'text': fields.String(required=True, description=(
        'This shows the user input. It concatenates all the previous'
        ' user input within the session with a *'
    ))
})


@ns.route('/')
class USSD(Resource):
    '''@see http://docs.africastalking.com/ussd'''

    @ns.doc('callback')
    @ns.expect(ussd)
    def post(self):
        '''USSD callback'''
        # get the required response message
        reply = logic.parse_and_reply(api.payload['text'])

        # log ussd message in the database
        logic.record(api.payload, reply)

        # send reply back to the phone number
        return reply, 200
