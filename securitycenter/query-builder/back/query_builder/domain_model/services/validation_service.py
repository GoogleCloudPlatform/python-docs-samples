import re
from datetime import datetime
import query_builder.application.default_settings as default_settings
from ..exceptions import (
    QBValidationError,
    QBNotFoundError
)

LOGGER = default_settings.configure_logger('validation_service')

DURATION_REGEX = re.compile(r"^\d+(?:[wdhms])(?:\+\d+(?:[wdhms]))*$")
ISO_DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S%z'
THRESHOLD_OPTIONS = ['lt', 'le', 'eq', 'ne', 'ge', 'gt']


def assert_existing_query(uuid, query):
    """Check if query passed is not empty"""
    if not query:
        raise QBNotFoundError('Query not found for uuid: {}'.format(uuid))


def validate_runnable_query(query):
    """Check if a query is OK to run on SCC client"""
    errors = {}
    if not query.steps:
        __add_error(errors, 'steps', 'Required at least one step')
    else:
        for step in query.steps:
            if step.compare_duration:
                __validate_duration(errors, step.compare_duration, step.order)
            if step.read_time and step.read_time.value:
                __validate_read_time(errors, step.read_time,
                                     step.order)
            __validate_threshold(errors, step.threshold, step.order)

    if errors:
        LOGGER.debug('Validation errors: %s', errors)
        raise QBValidationError(errors)


def validate_save_query(query):
    """Check if a query is OK to be saved"""
    errors = {}
    if not query.name:
        __add_error(errors, 'name', 'Field name required')
    if not query.description:
        __add_error(errors, 'description', 'Field description required')

    try:
        validate_runnable_query(query)
    except QBValidationError as ex:
        ex.errors.update(errors)
        raise ex

    if errors:
        LOGGER.debug('Validation errors: %s', errors)
        raise QBValidationError(errors)


def __validate_duration(errors, duration, order):
    if not DURATION_REGEX.match(duration):
        __add_error(errors, 'compareDuration',
                    'Compare duration field invalid on step #{}'.format(order),
                    order)


def __validate_read_time(errors, read_time, order):
    _type = read_time.get_type()
    value = read_time.value
    if (_type == 'FROM_NOW' and not DURATION_REGEX.match(value)
            or _type == 'TIMESTAMP' and not __check_datetime(value)):
        __add_error(errors, 'readTimeValue',
                    'Read time field invalid on step #{}'.format(order),
                    order)


def __validate_threshold(errors, threshold, order):
    if threshold:
        if threshold.operator not in THRESHOLD_OPTIONS:
            __add_error(errors, 'thresholdOperator',
                        'Threshold operator field invalid on step #{}. Valid {}'
                        .format(order, THRESHOLD_OPTIONS),
                        order)
        if not threshold.value:
            __add_error(errors, 'thresholdValue',
                        'Threshold value field required on step #{}'
                        .format(order),
                        order)
        elif not threshold.value.isdecimal():
            __add_error(errors, 'thresholdValue',
                        'Threshold value field invalid on step #{}'
                        .format(order),
                        order)
    else:
        __add_error(errors, 'threshold',
                    'Threshold is empty on step #{}'.format(order),
                    order)


def __add_error(errors, field, msg, order=''):
    errors['{}{}'.format(field, order)] = {
        'message' : msg
    }


def __check_datetime(value):
    try:
        datetime.strptime(value, ISO_DATETIME_PATTERN)
    except ValueError:
        return False
    return True
