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

import endpoints
import mock
from protorpc import message_types
import pytest

import main


def test_echo():
    api = main.EchoApi()
    request = main.EchoApi.echo.remote.request_type(content='Hello world!')
    response = api.echo(request)
    assert 'Hello world!' == response.content


def test_get_user_email():
    api = main.EchoApi()

    with mock.patch('main.endpoints.get_current_user') as user_mock:
        user_mock.return_value = None
        with pytest.raises(endpoints.UnauthorizedException):
            api.get_user_email(message_types.VoidMessage())

        user_mock.return_value = mock.Mock()
        user_mock.return_value.email.return_value = 'user@example.com'
        response = api.get_user_email(message_types.VoidMessage())
        assert 'user@example.com' == response.content
