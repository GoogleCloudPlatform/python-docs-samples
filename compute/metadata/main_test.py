# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import requests

import main


@mock.patch('main.requests')
def test_wait_for_maintenance(requests_mock):
    # Host maintenance event start.
    event_start_mock = mock.Mock()
    event_start_mock.status_code = 200
    event_start_mock.text = 'MIGRATE_ON_HOST_MAINTENANCE'
    event_start_mock.headers = {'etag': 1}

    # Host maintenance event end.
    event_end_mock = mock.Mock()
    event_end_mock.status_code = 200
    event_end_mock.text = 'NONE'
    event_end_mock.headers = {'etag': 2}

    # Server unavailable (HTTP 503)
    server_unavailable_mock = mock.Mock()
    server_unavailable_mock.status_code = 503

    # Network error
    requests_mock.ConnectionError = requests.ConnectionError
    network_error = requests_mock.ConnectionError('connection reset by peer')

    requests_mock.codes.ok = requests.codes.ok
    requests_mock.get.side_effect = [
        network_error, event_start_mock, network_error, event_end_mock,
        network_error, server_unavailable_mock, network_error, event_end_mock,
        network_error, StopIteration()]

    callback_mock = mock.Mock()

    try:
        main.wait_for_maintenance(callback_mock)
    except StopIteration:
        pass

    assert callback_mock.call_count == 2
    assert callback_mock.call_args_list[0][0] == (
        'MIGRATE_ON_HOST_MAINTENANCE',)
    assert callback_mock.call_args_list[1][0] == (None,)
