import mock
import requests
import json

import detect_legacy_usage

@mock.patch('detect_legacy_usage.requests')
@mock.patch('detect_legacy_usage.time')
def test_wait_for_legacy_usage(time_mock, requests_mock):
    #Response 1 is a 404
    response1_mock = mock.Mock()
    response1_mock.status_code = 404
    #Response 2 is a 503
    response2_mock = mock.Mock()
    response2_mock.status_code = 503
    #Response 3 is a 200 with no change (all 0s)
    response3_data = {'0.1': 0, 'v1beta1': 0}
    response3_mock = mock.Mock()
    response3_mock.status_code = 200
    response3_mock.text = json.dumps(response3_data)
    response3_mock.headers = {'etag': 1}
    #Response 4 is a 200 with different data
    response4_data = {'0.1': 0, 'v1beta1': 1}
    response4_mock = mock.Mock()
    response4_mock.status_code = 200
    response4_mock.text = json.dumps(response4_data)
    response4_mock.headers = {'etag': 2}

    #Response 5 has another change
    response5_data = {'0.1': 1, 'v1beta1': 1}
    response5_mock = mock.Mock()
    response5_mock.status_code = 200
    response5_mock.text = json.dumps(response5_data)
    response5_mock.headers = {'etag': 3}

    requests_mock.codes.ok = requests.codes.ok
    #Repeat last response to make sure callback isn't called (no change)
    requests_mock.get.side_effect = [
        response1_mock, response2_mock, response3_mock, response4_mock,
        response5_mock, response5_mock, StopIteration()]



    callback_mock = mock.Mock()

    try:
        detect_legacy_usage.wait_for_legacy_usage(callback_mock)
    except StopIteration:
        pass

    assert callback_mock.call_count == 2
    assert callback_mock.call_args_list[0][0] == (response4_data,)
    assert callback_mock.call_args_list[1][0] == ({'0.1': 1, 'v1beta1': 0},)
    assert time_mock.sleep.call_count == 2
    assert time_mock.sleep.call_args_list[0][0] == (3600,)
    assert time_mock.sleep.call_args_list[1][0] == (1,)