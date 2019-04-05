import base64
import datetime
import os

import pytest
from google.protobuf import duration_pb2, timestamp_pb2

import client.scc_client_alpha as scc


ACCOUNT_SET = pytest.mark.skipif(
    not os.path.isfile(os.environ.get(
        'SCC_SA_CLIENT_FILE',
        'accounts/cscc_api_client.json'
    )),
    reason='SCC account not specified'
)


@pytest.fixture
def mock_datetime():
    return datetime.datetime(2018, 6, 1)


@ACCOUNT_SET
@pytest.mark.parametrize('duration', ['40w', '280d', '6720h', '403200m', '24192000s'])
def test_create_scc_params_durations(mocker, mock_datetime, duration):
    # given
    client = scc.Client()
    expected = {
        'query' : 'attribute.asset_type = "PROJECT"',
        'compare_duration' : duration_pb2.Duration(seconds=24192000)
    }
    # when
    with mocker.patch('client.helpers.now', return_value=mock_datetime):
        result = client.create_scc_params(
            where='attribute.asset_type = "PROJECT"',
            duration=duration)
        # then
        assert expected == result, 'The result should be equals: {}'.format(str(expected))


@ACCOUNT_SET
def test_create_scc_params_ref_from_now(mocker, mock_datetime):
    # given
    client = scc.Client()
    expected = {
        'query' : 'attribute.asset_type = "PROJECT"',
        'compare_duration' : duration_pb2.Duration(seconds=24192000),
        'reference_time' : timestamp_pb2.Timestamp(seconds=1527807600)
    }
    # when
    with mocker.patch('client.helpers.now', return_value=mock_datetime):
        result = client.create_scc_params(
            where='attribute.asset_type = "PROJECT"',
            duration='40w',
            reference_time='1h',
            reference_time_type='FROM_NOW')
        # then
        assert expected == result, 'The result should be equals: {}'.format(str(expected))


@ACCOUNT_SET
def test_create_scc_params_ref_timestamp():
    # given
    client = scc.Client()
    expected = {
        'query' : 'attribute.asset_type = "PROJECT"',
        'compare_duration' : duration_pb2.Duration(seconds=24192000),
        'reference_time' : timestamp_pb2.Timestamp(seconds=1527811200)
    }
    # when
    result = client.create_scc_params(
        where='attribute.asset_type = "PROJECT"',
        duration='40w',
        reference_time='2018-06-01T00:00:00+0000',
        reference_time_type='TIMESTAMP')
    # then
    assert expected == result, 'The result should be equals: {}'.format(str(expected))


@ACCOUNT_SET
def test_execute_cscc_search_asset():
    # given
    client = scc.Client()
    where = 'attribute.asset_type = "PROJECT"'
    kind = client.ASSET_KIND
    # when
    result = client.execute_cscc_search(kind=kind, query_args={'query' : where})
    # then
    assert len(result) > 0, 'Should return at least one item.'


@ACCOUNT_SET
def test_execute_cscc_search_finding():
    # given
    client = scc.Client()
    where = 'attribute.scanner_id = "GOOGLE_ANOMALY_DETECTION"'
    kind = client.FINDING_KIND
    # when
    result = client.execute_cscc_search(kind=kind, query_args={'query' : where})
    # then
    assert len(result) > 0, 'Should return at least one item.'


@ACCOUNT_SET
def test_add_or_update_marks_asset(mocker):
    # given
    client = scc.Client()
    uuid = '66d849aa-f121-40f3-911b-95127bc3a03a'
    marks = {'scc_query_{}'.format(uuid): 'working_{}'.format(uuid)}
    ids_by_kind = {
        client.ASSET_KIND: set(['marine-physics-196005/instance/6515504379959957375'])
    }
    # when
    with mocker.mock_module.patch('google.cloud.securitycenter.SecurityCenterClient.modify_asset') as mock:
        client.add_or_update_marks(marks=marks, ids_by_kind=ids_by_kind)
        # then
        mock.assert_called()


@ACCOUNT_SET
def test_add_or_update_marks_finding(mocker):
    # given
    client = scc.Client()
    uuid = '66d849aa-f121-40f3-911b-95197bc3a05a'
    marks = {'scc_query_{}'.format(uuid): 'working_{}'.format(uuid)}
    ids_by_kind = {
        client.FINDING_KIND: set(['688851828130-cat-0111/cloud/project_id/white-list-195009/policy_violation/COIN_MINING'])
    }
    # when
    with mocker.mock_module.patch('google.cloud.securitycenter.SecurityCenterClient.modify_finding') as mock:
        client.add_or_update_marks(marks=marks, ids_by_kind=ids_by_kind)
        # then
        mock.assert_called()


def test_get_service_account_from_env():
    original_service_account = '{"data": "fdj2i3ff1"}'
    os.environ['SCC_SERVICE_ACCOUNT'] = original_service_account
    service_account = scc.get_service_account_json()

    assert service_account is not None
    assert service_account['data'] == "fdj2i3ff1"


def test_get_service_account_from_env_fail():
    original_service_account = "{\"data\": \"fdj2i3ff1\"}"
    del os.environ["SCC_SERVICE_ACCOUNT"]
    service_account = scc.get_service_account_json()

    assert service_account is None
    assert service_account != original_service_account


@ACCOUNT_SET
def test_execute_cscc_search_finding_with_timeout_error():
    # given
    client = scc.Client()
    kind = client.FINDING_KIND
    # when
    with pytest.raises(Exception) as excinfo:
        client.execute_cscc_search(kind=kind, query_args={'timeout' : 1, 'retry' : None})
    # then
    assert 'Deadline Exceeded' in str(excinfo.value), 'Should raise Deadline Exceeded error.'