"""Creates a dict with the arguments to the search assets method."""
from client import helpers as scc_helpers

FINDING_FROM_LAST_EXECUTION = "eventTime>={} AND eventTime<={} AND "
FINDING_FROM_LAST_EXECUTION_INITIAL = "eventTime<={} AND "

def build_api_call_args(_step, query_join='', now=None, last_execution=None):
    query_args = {'query': _step.get('where') + query_join}

    if _step.get('duration'):
        duration = scc_helpers.duration_to_seconds(_step.get('duration'))
        query_args['compare_duration'] = '{}s'.format(duration)

    reference_time = _step.get('referenceTime')
    if reference_time:
        if reference_time.get('type').upper() == 'TIMESTAMP':
            # convert datetime to UTC
            query_args['reference_time'] = scc_helpers.datetime_to_utc(reference_time.get('value'))
        if reference_time.get('type').upper() == 'FROM_NOW':
            duration = scc_helpers.duration_to_seconds(reference_time.get('value'))
            query_args['reference_time'] = scc_helpers.from_now_to_datetime_utc(duration)

    from_last_execution = _step.get('fromLastJobExecution')
    if from_last_execution:
        if _step.get('kind') == 'ASSET':
            print('From Last Job Execution setting not available to Asset query steps.')
        else:
            interval_condition = ""
            if last_execution:
                interval_condition = FINDING_FROM_LAST_EXECUTION.format(last_execution, now)
            else:
                interval_condition = FINDING_FROM_LAST_EXECUTION_INITIAL.format(now)
            query_args['query'] = interval_condition + query_args['query']
    return query_args
