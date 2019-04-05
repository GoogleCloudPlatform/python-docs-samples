import google.cloud.datastore.entity as ds_entity
import google.cloud.datastore.key as ds_key
import pytest

from creator.query.query_executor import process_query
from creator.gcp.db_services import set_query_last_execution

def make_query(qname):
    key = ds_key.Key('EntityKind', 1234, project='project')
    two_step_query = ds_entity.Entity(key=key)
    two_step_query['name'] = qname
    return two_step_query


def make_threshold(operator, value):
    threshold = ds_entity.Entity()
    threshold['operator'] = operator
    threshold['value'] = value
    return threshold


def make_join(kind, order, type, field):
    first_join = ds_entity.Entity()
    first_join['kind'] = kind
    first_join['field'] = field
    first_join['order'] = order
    first_join['type'] = type
    return first_join


def make_step(kind, order, where, ref_time_type=None, ref_time_value=None,
              duration=None, fromLastExecution=None):
    first_step = ds_entity.Entity()
    first_step['kind'] = kind
    first_step['order'] = order
    first_step['where'] = where
    if ref_time_type and ref_time_value:
        first_step['referenceTime'] = make_reference_time(ref_time_type,
                                                          ref_time_value)
    if duration:
        first_step['duration'] = duration
    if fromLastExecution:
        first_step['fromLastJobExecution'] = fromLastExecution
    return first_step

def test_finding_with_form_last_executiuon():
    pytest.skip("skip integration tests")
    query = make_query("query findings")

    query['joins'] = [
        (make_join('FINDING', 1, 'SINGLE', 'resourceName'))]

    query['steps'] = [
        (make_step('FINDING', 1, 'category = "resource_involved_in_coin_mining"', fromLastExecution='true'))
        ]
    query['threshold'] = make_threshold('gt', 1000000)
    #set_query_last_execution(query,1550589452000)
    response = process_query(query)