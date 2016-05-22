import logging

from app import settings
from app.signatures import cert_chain_url_valid, parse_certificate, signature_valid

logger = logging.getLogger(__name__)


class AlexaRequest():
    intent_name = None
    slots = None

    def __init__(self, flask_request):
        self.flask_request = flask_request
        self.data = flask_request.json
        if not self.data:
            raise ValueError('no data received!')
        self.request_type = self.data['request']['type']
        self.session = self.data['session']
        self.timestamp = self.data['request']['timestamp']
        if self.request_type == 'IntentRequest':
            self.intent_name = self.data['request']['intent']['name']
            self.slots = self.data['request']['intent'].get('slots')

    def is_valid(self):
        # check Application ID
        sent_id = self.session['application']['applicationId']
        if sent_id != settings.AMAZON_APPLICATION_ID:
            # TODO: log
            return False

        # check timestamp
        # TODO!

        # check certificate URL
        cert_chain_url = self.flask_request.headers.get('SignatureCertChainUrl')
        if not cert_chain_url_valid(cert_chain_url):
            # TODO: log
            return False

        # check signature
        signature = self.flask_request.headers.get('Signature')
        cert_text = parse_certificate(cert_chain_url)
        request_body = self.flask_request.data
        if not signature_valid(signature, cert_text, request_body):
            # TODO: log
            return False

        return True


class AlexaResponse():
    card_text = None
    card_title = None
    ends_session = True
    reprompt_speech = None
    response_version = settings.SKILL_VERSION
    speech = None

    def __init__(self, speech_text, ends_session=True):
        self.speech = speech_text
        self.ends_session = ends_session
        self.session_attributes = {}

    def add_to_session(self, key, val):
        self.session_attributes[key] = val

    def card(self, title, text):
        self.card_title = title
        self.card_text = text

    def get_card_dict(self):
        return {
            'type': 'Simple',
            'title': self.card_title,
            'content': self.card_text,
        }

    def get_reprompt_dict(self):
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': self.reprompt_speech,
            },
        }

    def reprompt(self, question):
        self.ends_session = False
        self.reprompt_speech = question

    def get_speech_dict(self):
        return {
            'type': 'PlainText',
            'text': self.speech,
        }

    def to_dict(self):
        data = {
            'response': {
                'outputSpeech': self.get_speech_dict(),
                'shouldEndSession': self.ends_session,
            },
            'sessionAttributes': self.session_attributes,
            'version': self.response_version,
        }
        if self.card_text:
            data['response'].update({'card': self.get_card_dict()})
        if self.reprompt_speech:
            data['response'].update({'reprompt': self.get_reprompt_dict()})
        return data
