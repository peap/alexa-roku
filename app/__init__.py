import logging

from flask import Flask, abort, g, jsonify, render_template, request

from app import settings
from app.roku import RokuError, find_roku_on_local_network

logger = logging.getLogger('alexa-roku')

app = Flask('alexa-roku')
app.config.from_object(settings)


@app.before_first_request
def get_local_roku_device():
    """Get the Roku on this network. Assumes only 1 exists, for now."""
    logger.info('Looking for a Roku device.')
    roku = find_roku_on_local_network()
    if roku is None:
        raise RokuError('Could not find a Roku on the local network!')
    logger.info('Found a Roku device: {0}'.format(roku))
    g.roku = roku


@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/alexa/', methods=['POST'])
def incoming_alexa_request():
    from app.alexa import AlexaRequest
    from app.handlers import dispatch
    try:
        alexa_request = AlexaRequest(request)
    except ValueError:
        abort(400)

    if alexa_request.is_valid():
        alexa_response = dispatch(alexa_request)
    else:
        abort(403)

    return jsonify(alexa_response.to_dict())
