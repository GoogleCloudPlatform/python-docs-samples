import json
import uuid as uuid_service
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    make_response
)

from query_builder.domain_model.adapters import (
    from_json_to_query_dto,
    from_model_to_query_json,
    from_model_to_simple_queries_json
)
import query_builder.domain_model.services.services_facade as service
from query_builder.domain_model.db import database
from query_builder.domain_model.exceptions import MissingSecurityHeadersError
from query_builder.domain_model.services.validation_service import (
    QBValidationError,
    QBNotFoundError
)
from query_builder.domain_model.services.scc_service import RunStepError


AUTHENTICATED_USER_EMAIL_HEADER = 'x-goog-authenticated-user-email'
AUTHENTICATED_USER_ID_HEADER = 'x-goog-authenticated-user-id'
IAP_JWT_ASSERTION_HEADER = 'x-goog-iap-jwt-assertion'

query_blueprint = Blueprint('query', __name__)


@query_blueprint.before_request
def before_request():
    validate_security_header()
    database.connect()


@query_blueprint.teardown_request
def teardown_request(response):
    if not database.is_closed():
        database.close()
    return response


@query_blueprint.route("/queries", methods=['GET'])
def list_queries():
    page = request.args.get('page', type=int)
    page_size = request.args.get('page_size', type=int)
    text = request.args.get('text')

    current_app.logger.info('listing queries')
    current_app.logger.info(
        "page: %s, page_size: %s, text: %s", page, page_size, text)

    queries, total = service.list_queries(
        page, page_size, text if text else '')

    result = from_model_to_simple_queries_json(queries, total)
    current_app.logger.info(result)
    return jsonify(result)


@query_blueprint.route("/queries/<uuid>", methods=['GET'])
def get_query(uuid):
    current_app.logger.info('getting query: %s', uuid)

    query = service.get_query(uuid)
    result = from_model_to_query_json(query)

    current_app.logger.info(result)
    return jsonify(result)


@query_blueprint.route("/queries", methods=['POST'])
def save_query():
    current_app.logger.info('saving query')

    data = set_uuid_if_none(set_owner(request.get_json()))
    dto = from_json_to_query_dto(data)
    query = service.save_query(dto)
    result = from_model_to_query_json(query)

    current_app.logger.info(result)
    return jsonify(result)


@query_blueprint.route("/queries/<uuid>", methods=['DELETE'])
def delete_query(uuid):
    current_app.logger.info('deleting query: %s', uuid)
    service.delete_query(uuid)
    return jsonify({})


@query_blueprint.route("/marks/clean/<uuid>", methods=['DELETE'])
def clean_up_mark(uuid):
    current_app.logger.info('cleaning marks for query: %s', uuid)
    service.clean_up_marks(uuid)
    return jsonify({})


@query_blueprint.route("/queries/run", methods=['POST'])
def run_query():
    current_app.logger.info('running query')
    request_mode = request.args.get('mode')
    mode = request_mode if request_mode else 'execution'
    data = set_uuid_if_none(set_owner(request.get_json()))
    dto = from_json_to_query_dto(data)
    uuid, total, url, mark, step_results = service.run_query(dto, mode)

    result = build_run_execution_response(uuid, mark, total, url, step_results)
    current_app.logger.info(result)
    return jsonify(result)


@query_blueprint.route("/queries/notify", methods=['PUT'])
def change_notify():
    data = request.get_json()
    service.update_query_notify(data.get('uuid'), data.get('notifyFlag'))

    return jsonify({})


@query_blueprint.route("/queries/run/<uuid>", methods=['POST'])
def run_query_by_id(uuid):
    current_app.logger.info('running query by id: %s', uuid)

    uuid_received, total, url, mark, step_results = service.run_query_by_uuid(uuid)
    result = build_run_execution_response(uuid_received, mark, total, url, step_results)

    current_app.logger.info(result)
    return jsonify(result)


@query_blueprint.route("/queries/scheduled/run", methods=['PUT'])
def run_scheduled_queries():
    current_app.logger.info('running scheduled queries')
    service.run_scheduled_queries()
    return make_response()


def build_run_execution_response(uuid, mark, total, url, step_results):
    return {
        'uuid': uuid,
        'result_size': total,
        'scc_query_link': url,
        'mark': mark,
        'stepResult': step_results
    }


def set_uuid_if_none(json_data):
    if not json_data.get('uuid'):
        json_data['uuid'] = uuid_service.uuid4()
    return json_data


def set_owner(json_data):
    owner = request.headers.get(AUTHENTICATED_USER_EMAIL_HEADER)
    split = owner.split(':') if owner else [
        'accounts.google.com', 'example@example.org']
    json_data['owner'] = split[1] if len(split) > 1 else owner
    return json_data


@query_blueprint.errorhandler(QBValidationError)
def handle_validation_errors(e):
    resp = jsonify(e.errors)
    resp.status_code = 400
    return resp


@query_blueprint.errorhandler(QBNotFoundError)
def handle_not_found_errors(e):
    resp = jsonify(e.errors)
    resp.status_code = 404
    return resp


@query_blueprint.errorhandler(RunStepError)
def handle_api_call_errors(e):
    resp = jsonify(e.error)
    resp.status_code = 400
    return resp


@query_blueprint.errorhandler(MissingSecurityHeadersError)
def handle_missing_security_headers(e):
    resp = jsonify(e.errors)
    resp.status_code = 403
    return resp


def validate_security_header():
    if current_app.config['FLASK_ENV'] != 'development' and (
            not request.headers.get(AUTHENTICATED_USER_EMAIL_HEADER) or
            not request.headers.get(AUTHENTICATED_USER_ID_HEADER) or
            not request.headers.get(IAP_JWT_ASSERTION_HEADER)
    ):
        raise MissingSecurityHeadersError("Access Denied.")
