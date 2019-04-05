import datetime
import os
import sys
import traceback
from time import sleep

from creator.gcp.db_services import get_event_queries
from creator.gcp.db_services import set_query_last_execution
from creator.gcp.db_services import get_query_last_execution
from creator.gcp.publish_services import publish_result
from creator.gcp.scc_service import execute_cscc_search
from creator.query.api_call_builder import build_api_call_args
from creator.query.query_process_helper import build_join, get_element_by_order
from client import helpers as scc_helpers


# Queries per Second allowed in the API calls
WAIT_TIME = 1 / float(os.getenv('QPS', '1000'))


def process_saved_queries():
    queries = get_event_queries()
    if queries:
        for query in queries:
            try:
                process_query(query)
            except Exception as e:
                print('Error processing query: {}'.format(query), file=sys.stderr)
                print('Error: {}'.format(e), file=sys.stderr)
                print(traceback.format_exc(), file=sys.stderr)
    else:
        print('No query for execution was found. Please upload a valid query.', file=sys.stderr)


def process_query(_query):
    steps = _query.get('steps')
    resp = None
    kind = None
    last_execution = get_query_last_execution(_query)
    execution_time = scc_helpers.unix_time_millis_whitout_timestamp(__now())*1000
    for step_order in range(1, len(steps) + 1):
        current_step = get_element_by_order(steps, step_order)

        query_join_for_step = build_join(resp, _query.get('joins'), step_order)

        if not query_join_for_step and step_order > 1:
            print('Unable to get join values for step #{}'.format(step_order))
            return

        query_step_args = build_api_call_args(current_step,
                                              query_join=query_join_for_step,
                                              now=execution_time,
                                              last_execution=last_execution)
        print('args: ' + str(query_step_args))

        kind = current_step.get('kind')

        resp = execute_cscc_search(kind, query_step_args)

        # wait some time not to pass the maximum QPS
        sleep(WAIT_TIME)

    if meet_the_threshold(len(resp), _query.get('threshold')):
        publish_result(resp, _query.get('topic'), kind, query_to_dict(_query, len(resp), __now()))
    else:
        print('Did not satisfied threshold condition')
    set_query_last_execution(_query, execution_time + 1)
    return resp


def query_to_dict(query, size, date):
    return {
        'name': or_no_set(query.get('name')),
        'last_execution_date': str(date),
        'last_execution_result': or_no_set(size),
        'last_execution_status': 'SUCCESS'
    }


def or_no_set(value):
    return value if value is not None else 'NOT_SET'


def meet_the_threshold(resp_size, threshold):
    if threshold:
        threshold_value = int(threshold.get('value'))
        options = {'lt': resp_size < threshold_value,
                   'le': resp_size <= threshold_value,
                   'eq': resp_size == threshold_value,
                   'ne': resp_size != threshold_value,
                   'ge': resp_size >= threshold_value,
                   'gt': resp_size > threshold_value
                   }
        return options.get(threshold.get('operator'), lambda: False)
    return False


def __now():
    return datetime.datetime.utcnow()
