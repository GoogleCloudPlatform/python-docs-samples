# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from unittest import mock
import requests

import detect_legacy_usage


def execute_test(requests_mock, *responses):
    callback_mock = mock.Mock()
    requests_mock.codes.ok = requests.codes.ok
    requests_mock.get.side_effect = responses + (StopIteration(),)
    try:
        detect_legacy_usage.wait_for_legacy_usage(callback_mock)
    except StopIteration:
        return callback_mock


@mock.patch('detect_legacy_usage.requests')
@mock.patch('detect_legacy_usage.time')
def test_metadata_server_unavailable(time_mock, requests_mock):
    # Metadata server unavailable
    response_mock = mock.Mock()
    response_mock.status_code = 503

    callback_mock = execute_test(requests_mock, response_mock)

    assert callback_mock.call_count == 0
    assert time_mock.sleep.call_count == 1
    assert time_mock.sleep.call_args_list[0][0] == (1,)


@mock.patch('detect_legacy_usage.requests')
@mock.patch('detect_legacy_usage.time')
def test_endpoint_does_not_exist(time_mock, requests_mock):
    # legacy-endpoint-access url unavailable (removed or not yet supported)
    response_mock = mock.Mock()
    response_mock.status_code = 404

    callback_mock = execute_test(requests_mock, response_mock)

    assert callback_mock.call_count == 0
    assert time_mock.sleep.call_count == 1
    assert time_mock.sleep.call_args_list[0][0] == (3600,)


@mock.patch('detect_legacy_usage.requests')
@mock.patch('detect_legacy_usage.time')
def test_callback_called_on_change(time_mock, requests_mock):
    # Response 1 has starting counts (should not trigger callback)
    response1_data = {'0.1': 5, 'v1beta1': 10}
    response1_mock = mock.Mock()
    response1_mock.status_code = 200
    response1_mock.text = json.dumps(response1_data)
    response1_mock.headers = {'etag': '1'}

    # Response 2 has different data
    response2_data = {'0.1': 6, 'v1beta1': 10}
    response2_mock = mock.Mock()
    response2_mock.status_code = 200
    response2_mock.text = json.dumps(response2_data)
    response2_mock.headers = {'etag': '2'}

    callback_mock = execute_test(requests_mock, response1_mock, response2_mock)

    # One change so callback is called once
    assert callback_mock.call_count == 1
    assert callback_mock.call_args_list[0][0] == ({'0.1': 1, 'v1beta1': 0},)
    assert time_mock.sleep.call_count == 0


@mock.patch('detect_legacy_usage.requests')
@mock.patch('detect_legacy_usage.time')
def test_callback_not_called_without_change(time_mock, requests_mock):
    # Response 1 has starting counts (should not trigger callback)
    response1_data = {'0.1': 5, 'v1beta1': 10}
    response1_mock = mock.Mock()
    response1_mock.status_code = 200
    response1_mock.text = json.dumps(response1_data)
    response1_mock.headers = {'etag': '1'}

    # Response 2 has the same data (no change)
    response2_mock = mock.Mock()
    response2_mock.status_code = 200
    response2_mock.text = json.dumps(response1_data)
    response2_mock.headers = {'etag': '1'}

    callback_mock = execute_test(requests_mock, response1_mock, response2_mock)

    # No change so callback is not called
    assert callback_mock.call_count == 0
    assert time_mock.sleep.call_count == 0
