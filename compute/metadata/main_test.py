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

from unittest import mock

import requests

import main


@mock.patch('main.requests')
def test_wait_for_maintenance(requests_mock):
    # Response 1 is a host maintenance event.
    response1_mock = mock.Mock()
    response1_mock.status_code = 200
    response1_mock.text = 'MIGRATE_ON_HOST_MAINTENANCE'
    response1_mock.headers = {'etag': 1}
    # Response 2 is the end of the event.
    response2_mock = mock.Mock()
    response2_mock.status_code = 200
    response2_mock.text = 'NONE'
    response2_mock.headers = {'etag': 2}
    # Response 3 is a 503
    response3_mock = mock.Mock()
    response3_mock.status_code = 503

    requests_mock.codes.ok = requests.codes.ok
    requests_mock.get.side_effect = [
        response1_mock, response2_mock, response3_mock, response2_mock,
        StopIteration()]

    callback_mock = mock.Mock()

    try:
        main.wait_for_maintenance(callback_mock)
    except StopIteration:
        pass

    assert callback_mock.call_count == 2
    assert callback_mock.call_args_list[0][0] == (
        'MIGRATE_ON_HOST_MAINTENANCE',)
    assert callback_mock.call_args_list[1][0] == (None,)
