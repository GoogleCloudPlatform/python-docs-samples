import google.cloud.datastore.entity as ds_entity
import pytest

from creator.query.query_executor import process_query

from tests.mock_queries import (
    mock_two_steps_asset_properties_query,
    mock_two_steps_asset_mark_query,
    mock_two_steps_asset_finding,
    mock_two_steps_asset_attribute_query,
    mock_two_steps_asset_attribute_mult_query,
    mock_one_step_asset_from_reference_time_timestamp,
    mock_one_step_finding_from_reference_time_fromnow,
    mock_two_step_asset_from_reference_time_with_duration
)

def make_query(qname):
    two_step_query = ds_entity.Entity()
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
              duration=None):
    first_step = ds_entity.Entity()
    first_step['kind'] = kind
    first_step['order'] = order
    first_step['where'] = where
    if ref_time_type and ref_time_value:
        first_step['referenceTime'] = make_reference_time(ref_time_type,
                                                          ref_time_value)
    if duration:
        first_step['duration'] = duration
    return first_step


def make_reference_time(rt_type, value):
    entity = ds_entity.Entity()
    entity['type'] = rt_type
    entity['value'] = value
    return entity

def test_two_steps_asset_properties_query(mocker):
    # given
    two_step_query = make_query("two step query for project join with properties")

    two_step_query['joins'] = [
        (make_join('ASSET', 1, 'SINGLE', 'resourceProperties.name')),
        (make_join('ASSET', 2, 'SINGLE', 'resourceProperties.name'))]

    two_step_query['steps'] = [
        (make_step('ASSET', 1, 'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" AND '
                               'securityCenterProperties.resourceOwners : "dandrade"')),
        (make_step('ASSET', 2, 'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project"'))]

    two_step_query['threshold'] = make_threshold('gt', 1000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_two_steps_asset_properties_query()) as mock:
        # when
        response = process_query(two_step_query)
        # then
        assert mock.called
        assert len(response) is not 0


def test_two_steps_asset_mark_query(mocker):
    #given
    two_step_query = make_query("two step query for project join with marks")

    two_step_query['joins'] = [
        (make_join('ASSET', 1, 'SINGLE', 'securityMarks.marks.scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f')),
        (make_join('ASSET', 2, 'SINGLE', 'securityMarks.marks.scc_query_6f04f632-3276-4ff3-b32a-92f794fb0f2f'))]

    two_step_query['steps'] = [
        (make_step('ASSET', 1, 'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" AND '
                               'securityCenterProperties.resourceOwners : "dandrade"')),
        (make_step('ASSET', 2, 'resourceProperties.projectId = "asset-dev-project"'))]

    two_step_query['threshold'] = make_threshold('gt', 1000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_two_steps_asset_mark_query()) as mock:
        # when
        response = process_query(two_step_query)
        # then
        assert mock.called
        assert len(response) is not 0


def test_two_steps_asset_finding(mocker):
    #given
    two_step_query = make_query("two step query with assets and findings")

    two_step_query['joins'] = [
        (make_join('ASSET', 1, 'SINGLE', 'securityCenterProperties.resourceName')),
        (make_join('FINDING', 2, 'SINGLE', 'resourceName'))]

    two_step_query['steps'] = [
        (make_step('ASSET', 1, 'securityCenterProperties.resourceType = "google.compute.Firewall"')),
        (make_step('FINDING', 2, 'securityMarks.marks.test-mark = "test-mark-value-sz"'))]

    two_step_query['threshold'] = make_threshold('gt', 1000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_two_steps_asset_finding()) as mock:
        # when
        response = process_query(two_step_query)
        # then
        assert mock.called
        assert len(response) is not 0


def test_two_steps_asset_attribute_query(mocker):
    two_step_query = make_query("two step query for project join with attributes")

    two_step_query['joins'] = [
        (make_join('ASSET', 1, 'SINGLE', 'resourceProperties.projectId')),
        (make_join('ASSET', 2, 'SINGLE', 'resourceProperties.projectId'))]

    two_step_query['steps'] = [
        (make_step('ASSET', 1, 'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" AND '
                               'securityCenterProperties.resourceOwners : "walves"')),
        (make_step('ASSET', 2, 'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project"'))]

    two_step_query['threshold'] = make_threshold('gt', 1000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_two_steps_asset_attribute_query()) as mock:
        # when
        response = process_query(two_step_query)
        # then
        assert mock.called
        assert len(response) is not 0


def test_two_steps_asset_attribute_mult_query(mocker):
    two_step_query = make_query("two step query for project join with attributes of type Mult")

    two_step_query['joins'] = [
        (make_join('ASSET', 1, 'MULT', 'securityCenterProperties.resourceOwners')),
        (make_join('ASSET', 2, 'MULT', 'securityCenterProperties.resourceOwners'))]

    two_step_query['steps'] = [
        (make_step('ASSET', 1, 'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" AND '
                               'securityCenterProperties.resourceOwners : "dandrade"')),
        (make_step('ASSET', 2, 'securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" '))]

    two_step_query['threshold'] = make_threshold('gt', 10000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_two_steps_asset_attribute_mult_query()) as mock:
        # when
        response = process_query(two_step_query)
        # then
        assert mock.called
        assert len(response) is not 0


def test_one_step_asset_from_reference_time_timestamp(mocker):
    step_query = make_query(
        "one step query for networks created before reference time")

    step_query['joins'] = [
        make_join('ASSET', 1, 'SINGLE',
                  'securityCenterProperties.resourceType')
    ]

    step_query['steps'] = [
        (make_step('ASSET', 1,
                   'securityCenterProperties.resourceType = "google.compute.Network"',
                   'timestamp', '2018-04-25T18:00:00+0400'))
    ]

    step_query['threshold'] = make_threshold('gt', 10000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_one_step_asset_from_reference_time_timestamp()) \
                as mock:
        # when
        response = process_query(step_query)
        # then
        assert mock.called
        assert len(response) is not 0
        for asset in response:
            assert asset.state == 'UNUSED'


def test_one_step_finding_from_reference_time_fromnow(mocker):
    step_query = make_query(
        "one step query for findings on category")

    step_query['joins'] = [
        make_join('FINDING', 1, 'SINGLE',
                  '')
    ]

    step_query['steps'] = [
        (make_step('FINDING', 1,
                   'category : "CONTAINER_RUNTIME_ANOMALY"',
                   'from_now', '2d+7h+20m'))
    ]

    step_query['threshold'] = make_threshold('gt', 10000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_one_step_finding_from_reference_time_fromnow()) \
                as mock:
        # when
        response = process_query(step_query)
        # then
        assert mock.called
        assert len(response) is not 0


def test_two_step_finding_from_reference_time_with_duration(mocker):
    step_query = make_query(
        "two step query for findings with category ADDED on buckets within "
        "a week from reference time")

    step_query['joins'] = [
        make_join('ASSET', 1, 'SINGLE',
                  'securityCenterProperties.resourceName'),
        make_join('FINDING', 2, 'SINGLE',
                  'resourceName')
    ]

    step_query['steps'] = [
        (make_step('ASSET', 1,
                   'securityCenterProperties.resourceType = "google.cloud.storage.Bucket"',
                   'timestamp', '2018-4-25T18:00:00-0800', '1w')),
        (make_step('FINDING', 2,
                   'category="ADDED"'))
    ]

    step_query['threshold'] = make_threshold('gt', 10000000)

    with mocker.mock_module.patch(
            target='tests.query_executor_test.process_query',
            return_value=mock_two_step_asset_from_reference_time_with_duration()) \
                as mock:
        # when
        response = process_query(step_query)
        # then
        assert mock.called
        assert len(response) is not 0
        for finding in response:
            assert finding.state != 'UNUSED'
