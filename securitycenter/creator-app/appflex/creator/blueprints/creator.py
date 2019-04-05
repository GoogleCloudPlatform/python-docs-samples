import json
import base64

from flask import (Blueprint, request)

from creator.logger_config import configure_logger
from creator.config_service import get_pubsub_token as validation_token
from creator.request_handler import (
    handle_cron_request,
    handle_pubsub_request,
    handle_status_config,
)

creator_blueprint = Blueprint('creator', __name__)

LOGGER = configure_logger('creator_blueprint')


@creator_blueprint.route('/')
def hello():
    return '', 204


@creator_blueprint.route('/events/processor', methods=['GET'])
def cron_handler():
    if request.headers.get('X-AppEngine-Cron') is None:
        return 'Forbidden', 403
    handle_cron_request()
    return '', 204


def current_request_token():
    return request.args.get('token', '')


@creator_blueprint.route('/_ah/push-handlers/receive_message', methods=['POST'])
def pubsub_handler():
    if current_request_token() != validation_token():
        return 'Invalid request: token required', 400
    print('Data: {}'.format(request.data.decode('utf-8')))
    handle_pubsub_request()
    return '', 204


@creator_blueprint.route('/_ah/push-handlers/set_status', methods=['POST'])
def set_status_config_handler():
    if current_request_token() != validation_token():
        return 'Invalid request: token required', 400
    try:
        payload = json.loads(request.data.decode('utf-8'))
        print('Data: {}'.format(payload))
        payload_data = json.loads(base64.b64decode(payload['message']['data']))
        handle_status_config(payload_data)
    except:
        LOGGER.exception("Unexpected error when saving status.")
    return '', 204
