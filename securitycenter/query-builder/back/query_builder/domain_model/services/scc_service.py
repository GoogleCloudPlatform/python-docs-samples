import datetime
import os
import re
from multiprocessing import Pool

import client.scc_client_beta as scc
import query_builder.application.default_settings as default_settings
from .configuration_service import get_organization_id
from .pubsub_service import publish_result
from ..exceptions import RunStepError
from ..helpers.datetime_helper import (
    datetime_to_utc,
    from_now_to_datetime_utc,
    duration_to_seconds
)

LOGGER = default_settings.configure_logger('scc_service')

JOIN_TYPE_SINGLE = 'SINGLE'
JOIN_TYPE_LIST = 'LIST'
LIST_FIELDS = ['attribute.owners']

FINDING_KIND = 'FINDING'
ASSET_KIND = 'ASSET'

# Represents the pool size used to make parallel requests to the SCC API
POOL_SIZE = int(os.getenv('SCC_REQUEST_POOL_SIZE', '4'))


def add_not_executed(step_results, steps_size):
    for i in range(1, steps_size + 1):
        if not step_results.get(i):
            step_results[i] = {
                'responseSize': 0, 'status': 'NOT_EXECUTED'
            }


def process_scc_query(query, marks, mode="execution"):
    """Process a given scc query and identify the items found with the given marks.
    Optimized so to not change items that already have been marked with the same marks."""
    total_size = 0
    out_join = None
    response = None
    step_result = {}
    response_ids = {
        ASSET_KIND: set(),
        FINDING_KIND: set()
    }
    query_successful = False
    result_kind = None
    result_response = {
        ASSET_KIND: [],
        FINDING_KIND: []
    }
    client = get_scc_client()

    for step in sorted(query.steps, key=lambda step: step.order):
        scc_params = build_scc_request_params(step)

        if step.order > 1:
            if not step.in_join:
                LOGGER.info('Unable to get join values for step %d.', step.order)
                return None

            join_where = build_join(
                response, step.in_join, out_join, scc_params.get('query'))
            scc_params['query'] = join_where

        try:
            LOGGER.info('Request filter: {}'.format(scc_params.get('query')))
            LOGGER.info('Request from {} searching {} behind'.format(
                        scc_params.get('read_time') if scc_params.get('read_time') else 'now',
                        scc_params.get('compare_duration') if scc_params.get('compare_duration') else 'none'))
            response = execute_scc_search(client, scc_params, step.kind)
        except Exception as ex:
            LOGGER.exception("Error execution cscc search")
            raise RunStepError(step.order, ex)

        out_join = step.out_join

        response_ids[step.kind].update(x.name for x in response)

        response_size = len(response)
        step_result[step.order] = {
            'responseSize': response_size, 'status': 'FAILED'
        }
        LOGGER.info('Found %d items on step #%s.', response_size, step.order)

        if not response_size:
            LOGGER.info('Stopping query because this step has no results.')
            break

        if not step.threshold_satisfied(response_size):
            LOGGER.info('Stopping query because results did not meet this step threshold.')
            break

        step_result[step.order]['status'] = 'SUCCESS'

        # Execute only if step is the last one executed with response
        if response and step.order == len(query.steps):
            query_successful = True
            result_kind = step.kind
            result_response[result_kind] = response
            # Count of items that will be marked
            total_size = len(response_ids[ASSET_KIND]) + len(response_ids[FINDING_KIND])

    if not query_successful:
        clear_response_ids(response_ids)
        LOGGER.info('Query has no total_size.')
        add_not_executed(step_result, len(query.steps))
    else:
        LOGGER.info('Total items found: %d.', total_size)

    add_or_update_marks(client, marks, response_ids)
    marks = build_mark_from_id(query.uuid)
    execution_date = __now()
    if query_successful and query.send_notification and mode != "draft":
        publish_result(
            query.owner,
            result_response,
            mark_to_query_filed(marks),
            query_to_dict(query, total_size, execution_date),
            query.topic
        )
    return total_size, result_kind, step_result, execution_date


def execute_scc_search(client, scc_params, kind):
    if kind == ASSET_KIND:
        return client.list_assets(filter_expression=scc_params.get('query'),
                                  read_time=scc_params.get('read_time'),
                                  compare_duration=scc_params
                                  .get('compare_duration'))
    if kind == FINDING_KIND:
        return client.list_findings(source='-',
                                    filter_expression=scc_params.get('query'),
                                    read_time=scc_params.get('read_time'))


def add_or_update_marks(client, marks, ids_by_kind):
    """Add or update marks on ids passed by kind"""
    pool = Pool(processes=POOL_SIZE)
    for kind, new_ids in ids_by_kind.items():
        old_ids = get_previous_execution_ids(client, kind, marks)
        to_remove = __diff_marked_items_ids(old_ids, new_ids)
        to_add = __diff_marked_items_ids(new_ids, old_ids)

        if kind == ASSET_KIND:
            LOGGER.debug('Asset marks to remove: {}'.format(to_remove))
            _remove_asset_marks(to_remove, pool, client, marks)
            LOGGER.debug('Asset marks to add: {}'.format(to_add))
            _add_asset_marks(to_add, pool, client, marks)

        elif kind == FINDING_KIND:
            LOGGER.debug('Finding marks to remove: {}'.format(to_remove))
            _remove_finding_marks(to_remove, pool, client, marks)
            LOGGER.debug('Finding marks to add: {}'.format(to_add))
            _add_finding_marks(to_add, pool, client, marks)


def _add_asset_marks(to_add, pool, client, marks):
    processed = []
    limit_count = 0
    for add_item in to_add:
        limit_count += 1
        result = pool.apply_async(client.update_asset_security_mark,
                                  args=(marks, None, add_item))
        processed.append(result)
        limit_count, processed = _get_async_result(limit_count, processed)


def _remove_asset_marks(to_remove, pool, client, marks):
    processed = []
    limit_count = 0
    for remove_item in to_remove:
        limit_count += 1
        result = pool.apply_async(client.remove_asset_security_mark,
                                  args=(marks, None, remove_item))
        processed.append(result)
        limit_count, processed = _get_async_result(limit_count, processed)


def _add_finding_marks(to_add, pool, client, marks):
    processed = []
    limit_count = 0
    for add_item in to_add:
        limit_count += 1
        result = pool.apply_async(client.update_finding_security_mark,
                                  args=(marks, None, None, add_item))
        processed.append(result)
        limit_count, processed = _get_async_result(limit_count, processed)


def _remove_finding_marks(to_remove, pool, client, marks):
    processed = []
    limit_count = 0
    for remove_item in to_remove:
        limit_count += 1
        result = pool.apply_async(client.remove_finding_security_mark,
                                  args=(marks, None, None, remove_item))
        processed.append(result)
        limit_count, processed = _get_async_result(limit_count, processed)


def _get_async_result(limit_count, results):
    if POOL_SIZE <= limit_count:
        for result in results:
            result.get()
        return _clear_processed_results(limit_count, results)
    else:
        return limit_count, results


def _clear_processed_results(limit_count, results):
    limit_count = 0
    results = []
    return limit_count, results


def get_previous_execution_ids(client, kind, marks):
    scc_params = {
        'query': mark_to_query_filed(marks)
    }
    response = execute_scc_search(client, scc_params, kind)
    return {x.name for x in response}


def build_scc_request_params(_step):
    query_args = {'query': _step.filter}

    if _step.compare_duration:
        duration = _step.compare_duration
        query_args['compare_duration'] = '{}s'.format(
            duration_to_seconds(duration))

    read_time = _step.read_time
    if read_time:
        if read_time.get_type().upper() == 'TIMESTAMP' and read_time.value:
            # convert datetime to UTC
            query_args['read_time'] = '{}Z'.format(
                datetime_to_utc(read_time.value))
        if read_time.get_type().upper() == 'FROM_NOW' and read_time.value:
            duration = duration_to_seconds(read_time.value)
            query_args['read_time'] = '{}Z'.format(
                from_now_to_datetime_utc(duration))

    return query_args


def get_scc_client():
    client = scc.Client(get_organization_id())
    return client


def query_to_dict(query, size, date):
    return {
        'uuid': or_no_set(query.uuid),
        'name': or_no_set(query.name),
        'description': or_no_set(query.description),
        'owner': or_no_set(query.owner),
        'topic': or_no_set(query.topic),
        'timestamp': or_no_set(query.timestamp),
        'schedule': or_no_set(query.schedule),
        'send_notification': or_no_set(query.send_notification),
        'last_execution_date': str(date),
        'last_execution_result': or_no_set(size),
        'last_execution_status': 'SUCCESS'
    }


def or_no_set(value):
    return value if value is not None else 'NOT_SET'


def clear_response_ids(resp_ids):
    resp_ids[ASSET_KIND].clear()
    resp_ids[FINDING_KIND].clear()


def normalize_field(field):
    return field.replace('attribute.', '').replace('mark.', 'marks.').replace('property.', 'properties.')


def join_type(join_field):
    return JOIN_TYPE_LIST if join_field in LIST_FIELDS else JOIN_TYPE_SINGLE


def build_join(resp, in_join, out_join, where):
    if not out_join:
        return ''

    join_values = []
    for val in resp:
        field_value = get_field_by_name(
            val, str(normalize_field(out_join)))
        if field_value:
            join_values.append(field_value)

    if JOIN_TYPE_SINGLE != join_type(out_join) and join_values:
        join_values = split_values(join_values)

    return create_and_or_query_from_values(
        in_join,
        join_type(out_join),
        join_values,
        where
    )


def get_field_by_name(obj, field_name):
    if '.' not in field_name:
        if obj is None:
            return None
        if hasattr(obj, 'get'):
            return obj.get(field_name)
        if hasattr(obj, '__getitem__'):
            return obj[field_name]
        return getattr(obj, field_name)
    spliced = str(field_name).split('.', maxsplit=1)
    return get_field_by_name(get_field_by_name(obj, spliced[0]), spliced[1])


def split_values(original_values):
    splited_values = []
    for val in original_values:
        splited_values.extend(val)
    return splited_values


def create_and_or_query_from_values(field_name, field_type, values, where):
    if not values:
        return ''
    compare_op = ' = ' if field_type == JOIN_TYPE_SINGLE else ' : '
    join = '( ' + ' OR '.join(create_compare(field_name, compare_op, values)) + ' )'
    if where:
        return where + ' AND ' + join
    return join


def create_compare(field_name, compare_op, values):
    for val in values:
        yield field_name + compare_op + '"' + val + '"'


def build_mark_from_id(_id):
    cleaned_id = __clean_id(_id)
    _key = 'sccquery{}'.format(cleaned_id)
    _value = 'true'
    return {_key: _value}


def build_temp_mark_from_id(_id):
    cleaned_id = __clean_id(_id)
    _key = 'sccquerydraft{}'.format(cleaned_id)
    _value = 'true'
    result = {_key: _value}
    _key_time = 'sccquerydrafttime{}'.format(cleaned_id)
    _value_time = str(__now().timestamp())
    result[_key_time] = _value_time
    return result


def mark_to_query_filed(marks):
    return ','.join(
        ['security_marks.marks.{}:"{}"'.format(
            k.lower(), v.lower()) for k, v in marks.items() if 'drafttime' not in k]
    )


def __clean_id(to_clean):
    return re.sub('[^A-Za-z0-9]+', '', str(to_clean)).lower()


def __now():
    dateString = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    return datetime.datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%S')


def __diff_marked_items_ids(minuend_ids, subtrahend_ids):
    if minuend_ids:
        return minuend_ids.difference(subtrahend_ids)
    return set()
