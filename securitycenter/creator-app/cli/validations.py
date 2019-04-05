
import re
import sys

from datetime import datetime

VALID_THRESHOLD_OPERATOR_VALUES = ['lt', 'le', 'eq', 'ne', 'ge', 'gt']

DURATION_REGEX = re.compile(r"^\d+(?:[wdhms])(?:\+\d+(?:[wdhms]))*$")
ISO_DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S%z'


def validate_yaml(stream):
    if not type(stream) == list:
        print_validation_failure("File should contain a list of event queries.")
        sys.exit(4)
    for event_query in stream:
        check_valid_keys(event_query.keys(), ['name', 'topic', 'joins', 'steps', 'threshold'], 'query')
        validate_query_name(event_query)
        validate_query_join(event_query)
        validate_query_step(event_query)
        validate_query_threshold(event_query)


def validate_query_name(event_query):
    if not event_query.get('name'):
        print_validation_failure("every query should have a name.")
        sys.exit(4)

def validate_query_threshold(event_query):
    if not event_query.get('threshold'):
        print_validation_failure(
            "query \"{}\" should have a threshold."
            .format(event_query.get('name')))
        sys.exit(4)
    else:
        check_valid_keys(event_query.get('threshold').keys(), ['operator', 'value'], 'threshold')
        validate_query_threshold_operator(event_query)
        validate_query_threshold_value(event_query)


def validate_query_threshold_value(event_query):
    threshold = event_query.get('threshold')
    if not threshold.get('value') and threshold.get('value') != 0:
        print_validation_failure(
            "query \"{}\" should have a threshold value."
            .format(event_query.get('name')))
        sys.exit(4)


def validate_query_threshold_operator(event_query):
    threshold = event_query.get('threshold')
    if not threshold.get('operator'):
        print_validation_failure(
            "query \"{}\" should have a threshold operator."
            .format(event_query.get('name')))
        sys.exit(4)
    else:
        if not threshold.get('operator') in VALID_THRESHOLD_OPERATOR_VALUES:
            print_validation_failure(
                "query \"{}\" threshold operator \"{}\" not valid. valid values are: "
                "'lt','le','eq','ne','ge','gt'."
                .format(event_query.get('name'), threshold.get('operator')))
            sys.exit(4)


def validate_query_step(event_query):
    if not event_query.get('steps'):
        print_validation_failure(
            "query \"{}\" should have steps."
            .format(event_query.get('name')))
        sys.exit(4)
    for step in event_query.get('steps'):
        check_valid_keys(step.keys(), ['fromLastJobExecution', 'duration', 'kind', 'order', 'referenceTime', 'where'], 'step')
        validate_query_step_kind(event_query, step)
        validate_query_step_order(event_query, step)
        validate_query_step_reference_time(event_query, step)
        if step.get('duration'):
            validate_duration_value(step.get('duration'), 'step.duration')
        if step.get('fromLastJobExecution'):
            validate_from_last_job_execution(step.get('kind'))


def validate_from_last_job_execution(kind):
    if kind != 'FINDING':
        print_validation_failure("step \"fromLastJobExecution\" only valid for \"FINDING\" kind")
        sys.exit(4)


def check_datetime(value):
    try:
        datetime.strptime(value, ISO_DATETIME_PATTERN)
    except ValueError:
        return False
    return True


def validate_timestamp_value(value, field):
    if not check_datetime(value):
        print_validation_failure(
            "Value \"{}\" for attribute \"{}\" is invalid. Valid example: '2018-02-28T10:30:42+0400'"
            .format(value, field))
        sys.exit(7)


def validate_query_step_reference_time(event_query, step):
    ref_time = step.get('referenceTime')
    if ref_time:
        validate_reference_time_type(event_query, ref_time)
        validate_reference_time_value(event_query, ref_time)


def validate_reference_time_value(event_query, ref_time):
    if not ref_time.get('value'):
        print_validation_failure(
            "query \"{}\" step.referenceTime is missing \"value\" information."
            .format(event_query.get('name')))
        sys.exit(4)
    else:
        validate_reference_time_value_by_type(ref_time)


def validate_reference_time_type(event_query, ref_time):
    if not ref_time.get('type'):
        print_validation_failure(
            "query \"{}\" step.referenceTime is missing \"type\" information."
            .format(event_query.get('name')))
        sys.exit(4)
    else:
        if not ref_time.get('type') in ['timestamp', 'from_now']:
            print_validation_failure(
                "query \"{}\" step.referenceTime.type value \"{}\" is invalid. "
                "Valid values are: 'timestamp', 'from_now'"
                .format(event_query.get('name'), ref_time.get('type')))
            sys.exit(4)


def validate_reference_time_value_by_type(ref_time):
    if ref_time.get('type') == 'from_now':
        validate_duration_value(
            ref_time.get('value'),
            "step.referenceTime.value with type 'from_now'")
    if ref_time.get('type') == 'timestamp':
        validate_timestamp_value(
            ref_time.get('value'),
            "step.referenceTime.value with type 'timestamp'")


def validate_query_step_order(event_query, step):
    if not step.get('order'):
        print_validation_failure(
            "query \"{}\" step is missing \"field\" information."
            .format(event_query.get('name')))
        sys.exit(4)


def validate_query_step_kind(event_query, step):
    if not step.get('kind'):
        print_validation_failure(
            "query \"{}\" step is missing \"field\" information."
            .format(event_query.get('name')))
        sys.exit(4)
    else:
        if not step.get('kind') in ['ASSET', 'FINDING']:
            print_validation_failure(
                "step \"kind\" value \"{}\" is invalid. valid values are: \"ASSET\" or \"FINDING\" "
                .format(step.get('kind')))
            sys.exit(4)


def validate_query_join(event_query):
    if not event_query.get('joins'):
        print_validation_failure(
            "query \"{}\" should have joins."
            .format(event_query.get('name')))
        sys.exit(4)
    for join in event_query.get('joins'):
        check_valid_keys(join.keys(), ['field', 'kind', 'order', 'type'], 'join')
        validate_query_join_field(event_query, join)
        validate_query_join_order(event_query, join)
        validate_query_join_type(event_query, join)
        validate_query_join_kind(event_query, join)


def validate_query_join_field(event_query, join):
    if not join.get('field'):
        print_validation_failure(
            "query \"{}\" join is missing \"field\" information."
            .format(event_query.get('name')))
        sys.exit(4)


def validate_query_join_order(event_query, join):
    if not join.get('order'):
        print_validation_failure(
            "query \"{}\" join is missing \"field\" information."
            .format(event_query.get('name')))
        sys.exit(4)


def validate_query_join_type(event_query, join):
    if not join.get('type'):
        print_validation_failure(
            "query \"{}\" join is missing \"field\" information."
            .format(event_query.get('name')))
        sys.exit(4)
    else:
        if not join.get('type') in ['SINGLE', 'MULTI']:
            print_validation_failure(
                "join \"type\" value \"{}\" is invalid. valid values are: \"SINGLE\" or \"MULTI\" "
                .format(join.get('type')))
            sys.exit(4)


def validate_query_join_kind(event_query, join):
    if not join.get('kind'):
        print_validation_failure(
            "query \"{}\" join is missing \"field\" information."
            .format(event_query.get('name')))
        sys.exit(4)
    else:
        if not join.get('kind') in ['ASSET', 'FINDING']:
            print_validation_failure(
                "join \"kind\" value \"{}\" is invalid. valid values are: \"ASSET\" or \"FINDING\" "
                .format(join.get('kind')))
            sys.exit(4)


def check_valid_keys(actual, valid, entity):
    for current_key in actual:
        if current_key not in valid:
            print_validation_failure(
                "unknown attribute \"{}\" in {}. valid attributes are {}"
                .format(current_key, entity, str(valid)))
            sys.exit(5)


def validate_duration_value(duration, field):
    if not DURATION_REGEX.match(duration):
        print_validation_failure(
            "Value \"{}\" for attribute \"{}\" is invalid. Valid examples: '4w+1d+1h','7d','1m+30s'"
            .format(duration, field))
        print_validation_failure("Valid time units are: (w)eeks, (d)ays, (h)ours, (m)inutes, (s)econds")
        sys.exit(6)


def validate_mode_values(mode):
    if mode not in ["PRODUCTION", "DEMO"]:
        print_validation_failure(
            "load.py: error: invalid mode value \"{}\". "
            "Valid values are \"PRODUCTION\" or \"DEMO\"".format(mode))
        sys.exit(2)


def print_validation_failure(value):
    print("\033[1;31;40m{}\033[0;0m".format(value))


def print_notice(value):
    print("\033[1;32;40m{}\033[0;0m".format(value))
