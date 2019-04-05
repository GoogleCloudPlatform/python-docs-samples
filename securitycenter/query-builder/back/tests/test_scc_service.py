import os

import pytest
from googleapiclient.errors import HttpError

from query_builder.domain_model.dtos import (
    ReadTime,
    Step,
    Query,
    Threshold
)
from query_builder.domain_model.services.scc_service import (
    process_scc_query,
    get_scc_client,
    add_or_update_marks
)

ACCOUNT_SET = pytest.mark.skipif(
    not os.path.isfile(os.environ.get(
        'SCC_SA_CLIENT_FILE',
        'accounts/cscc_api_client.json'
    )),
    reason='SCC account not specified'
)


@ACCOUNT_SET
def test_process_scc_query_single_step():
    # given
    uuid = '6f04f63232764ff3b32a92f794fb0f2f'
    read_time = ReadTime(
        "TIMESTAMP",
        "2018-11-01T01:00:00-0200",
        "são paulo"
    )
    step = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        compare_duration='2w',
        filter_='securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" AND '
              'securityCenterProperties.resourceOwners : "ciandt" AND '
              'resourceProperties.name : "tools"',
        read_time=read_time,
        threshold=Threshold(operator="ge", value="0")
    )
    query = Query(
        uuid=uuid,
        name='Find projects on organization',
        steps=[step]
    )

    # when
    result, result_kind, step_result, _ = process_scc_query(query, {
        'sccquerycit{}'.format(uuid): 'workingcit{}'.format(uuid)
    })

    # then
    assert 1 == len(step_result)
    assert result == step_result[1]['responseSize']
    assert 'ASSET' == result_kind
    assert 'SUCCESS' == step_result[1]['status']


@ACCOUNT_SET
@pytest.mark.xfail(raises=HttpError)
def test_process_scc_query_with_invalid_marks():
    # given
    uuid = '6f04f632-3276-4ff3-b32a-92f794fb0f2f'
    step = Step(
        uuid=uuid,
        order=1,
        kind='FINDING',
        threshold=Threshold(operator="ge", value="0")
    )
    query = Query(
        uuid=uuid,
        name='All findings',
        steps=[step]
    )

    # when
    result, result_kind, step_result, _ = process_scc_query(query, {
        'sccquerycit{}'.format(uuid): 'workingcit{}'.format(uuid)
    })

    # then expect HttpError 400


@ACCOUNT_SET
def test_process_scc_query_two_steps():
    # given
    uuid = '293f42e2089c4f4491db881e961ca0ca'
    read_time = ReadTime(
        "FROM_NOW",
        "1h",
        "são paulo"
    )
    step1 = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        compare_duration='40w',
        filter_='resourceProperties.name : "notifier"',
        read_time=read_time,
        out_join='securityCenterProperties.resourceParent',
        threshold=Threshold(operator="ge", value="0")
    )
    step2 = Step(
        uuid=uuid,
        order=2,
        kind='FINDING',
        read_time=read_time,
        in_join='resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    query = Query(
        uuid=uuid,
        name='Find projects on organization',
        steps=[step2, step1]
    )

    # when
    result, result_kind, step_result, _ = process_scc_query(query, {
        'sccquery2step{}'.format(uuid): 'working2step{}'.format(uuid)
    })

    # then
    assert 2 == len(step_result)
    assert 'FINDING' == result_kind
    assert 'SUCCESS' == step_result[1]['status']
    assert 'SUCCESS' == step_result[2]['status']


@ACCOUNT_SET
def test_process_scc_query_two_steps_no_final_result():
    # given
    uuid = '386fa8353a0c4840a727fb13e013601a'
    read_time = ReadTime(
        "FROM_NOW",
        "1h",
        "são paulo"
    )
    step1 = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        compare_duration='40w',
        filter_='securityCenterProperties.resourceType = "INSTANCE" AND '
              'securityCenterProperties.resourceName = "marine-physics-196005/instance/6515504379959957375"',
        read_time=read_time,
        out_join='securityCenterProperties.resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    step2 = Step(
        uuid=uuid,
        order=2,
        kind='FINDING',
        filter_='category = "FOO"',
        read_time=read_time,
        in_join='resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    query = Query(
        uuid=uuid,
        name='Find projects on organization',
        steps=[step2, step1]
    )

    # when
    result, _, _, _ = process_scc_query(query, {
        'sccquery{}'.format(uuid): 'working{}'.format(uuid)
    })

    # then
    assert result == 0, 'Should has empty return.'


@ACCOUNT_SET
def test_process_scc_query_two_steps_no_final_result_2():
    # given
    uuid = '74b8f5a8982948fb9acc6377ecf5149a'
    step1 = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        filter_='securityCenterProperties.resourceType = "google.cloud.resourcemanager.Project" AND '
              'securityCenterProperties.resourceOwners : "blabla"',
        out_join='securityCenterProperties.resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    step2 = Step(
        uuid=uuid,
        order=2,
        kind='FINDING',
        in_join='resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    query = Query(
        uuid=uuid,
        name='query_test',
        description='testing',
        steps=[step2, step1]
    )

    # when
    result, _, _, _ = process_scc_query(query, {
        'sccquery{}'.format(uuid): 'working{}'.format(uuid)
    })

    # then
    assert result == 0, 'Should has empty return.'


@ACCOUNT_SET
def test_process_scc_query_three_steps():
    # given
    uuid = '74b8f5a8123450fb9acc6377ecf5159b'
    step1 = Step(
        uuid=uuid,
        order=1,
        kind='FINDING',
        filter_='category : "PROJECT_ACCESS"',
        out_join='resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    step2 = Step(
        uuid=uuid,
        order=2,
        kind='ASSET',
        in_join='name',
        out_join='name',
        threshold=Threshold(operator="ge", value="0")
    )
    step3 = Step(
        uuid=uuid,
        order=3,
        kind='FINDING',
        in_join='resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    query = Query(
        uuid=uuid,
        name='Find projects on organization',
        steps=[step3, step2, step1]
    )

    # when
    result, result_kind, step_result, _ = process_scc_query(query, {
        'sccquerytest{}'.format(uuid): 'workingtest{}'.format(uuid)
    })

    # then
    assert result > 0, 'Should return at least one item.'
    assert 'FINDING' == result_kind
    assert 3 == len(step_result)
    assert 'SUCCESS' == step_result[1]['status']
    assert 'SUCCESS' == step_result[2]['status']
    assert 'SUCCESS' == step_result[3]['status']


@ACCOUNT_SET
def test_process_scc_query_three_steps_with_all_ports_allowed_firewall_rule():
    # given
    uuid = '74b8f5a8982948fb9acc63775485149f'
    step1 = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        filter_='securityCenterProperties.resourceType = "google.compute.Firewall" AND '
              'resourceProperties.allowed : "0-65535" AND '
              'securityCenterProperties.resourceOwners : "an"',
        out_join='securityCenterProperties.resourceParent',
        threshold=Threshold(operator="ge", value="0")
    )
    step2 = Step(
        uuid=uuid,
        order=2,
        kind='ASSET',
        filter_='securityCenterProperties.resourceType = "google.compute.Instance"',
        in_join='securityCenterProperties.resourceParent',
        out_join='name',
        threshold=Threshold(operator="ge", value="0")
    )
    step3 = Step(
        uuid=uuid,
        order=3,
        kind='FINDING',
        filter_='category : "audit_log"',
        in_join='resourceName',
        threshold=Threshold(operator="ge", value="0")
    )
    query = Query(
        uuid=uuid,
        name='Find projects on organization',
        steps=[step3, step2, step1]
    )

    # when
    result, result_kind, step_result, _ = process_scc_query(query, {
        'sccquery{}'.format(uuid): 'working{}'.format(uuid)
    })

    # then
    assert result > 0, 'Should return at least one item.'


@ACCOUNT_SET
def test_process_scc_query_three_steps_with_all_ports_allowed_firewall_rule_fail_threshold():
    # given
    uuid = '74b8f5a8982948fb9acc63775485149f'
    step1 = Step(
        uuid=uuid,
        order=1,
        kind='ASSET',
        filter_='securityCenterProperties.resourceType = "google.compute.Firewall" AND '
              'resourceProperties.allowed : "0-65535" AND '
              'securityCenterProperties.resourceOwners : "an"',
        out_join='securityCenterProperties.resourceParent',
        threshold=Threshold(operator="ge", value="0")
    )
    step2 = Step(
        uuid=uuid,
        order=2,
        kind='ASSET',
        filter_='securityCenterProperties.resourceType = "google.compute.Instance" AND '
              'resourceProperties.zone : "central"',
        in_join='securityCenterProperties.resourceParent',
        out_join='name',
        threshold=Threshold(operator="ge", value="0")
    )
    step3 = Step(
        uuid=uuid,
        order=3,
        kind='FINDING',
        filter_='category : "audit_log"',
        in_join='resourceName',
        threshold=Threshold(operator="ge", value="100")
    )
    query = Query(
        uuid=uuid,
        name='Find projects on organization',
        steps=[step3, step2, step1]
    )

    # when
    result, _, step_results, _ = process_scc_query(query, {
        'sccquery{}'.format(uuid): 'working{}'.format(uuid)
    })

    # then
    assert result == 0, 'Should return no items.'
    assert len(step_results) == 3, 'Should have executed all steps.'
    assert int(step_results[2]['responseSize']) > 0, 'Last step must not be empty.'


@ACCOUNT_SET
def test_add_or_update_marks():
    # given
    client = get_scc_client()
    marks = {
        'sccquery999999999999' : '999999999999'
    }
    ids_by_kind = {
        'ASSET' : set(['organizations/1055058813388/assets/7490807736616395628']),
        'FINDING' : set(['organizations/1055058813388/sources/9264282320683959279/findings/a0a0a0a0a0a7']),
    }

    # when
    add_or_update_marks(client, marks, ids_by_kind)
