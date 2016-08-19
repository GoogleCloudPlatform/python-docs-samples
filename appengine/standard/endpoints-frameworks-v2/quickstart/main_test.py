# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
from protorpc import message_types

import main


def test_list_greetings(testbed):
    api = main.GreetingApi()
    response = api.list_greetings(message_types.VoidMessage())
    assert len(response.items) == 2


def test_get_greeting(testbed):
    api = main.GreetingApi()
    request = main.GreetingApi.get_greeting.remote.request_type(id=1)
    response = api.get_greeting(request)
    assert response.message == 'goodbye world!'


def test_multiply_greeting(testbed):
    api = main.GreetingApi()
    request = main.GreetingApi.multiply_greeting.remote.request_type(
        times=4,
        message='help I\'m trapped in a test case.')
    response = api.multiply_greeting(request)
    assert response.message == 'help I\'m trapped in a test case.' * 4


def test_authed_greet(testbed):
    api = main.AuthedGreetingApi()

    with mock.patch('main.endpoints.get_current_user') as user_mock:
        user_mock.return_value = None
        response = api.greet(message_types.VoidMessage())
        assert response.message == 'Hello, Anonymous'

        user_mock.return_value = mock.Mock()
        user_mock.return_value.email.return_value = 'user@example.com'
        response = api.greet(message_types.VoidMessage())
        assert response.message == 'Hello, user@example.com'
