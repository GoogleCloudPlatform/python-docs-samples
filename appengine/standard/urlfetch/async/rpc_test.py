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


from google.appengine.api import urlfetch
import mock
import pytest
import webtest

import rpc


@pytest.fixture
def app():
    return webtest.TestApp(rpc.app)


@mock.patch('rpc.urlfetch')
def test_url_fetch(urlfetch_mock, app):
    get_result_mock = mock.Mock(
        return_value=mock.Mock(
            status_code=200,
            content='I\'m Feeling Lucky'))
    urlfetch_mock.create_rpc = mock.Mock(
        return_value=mock.Mock(get_result=get_result_mock))
    response = app.get('/')
    if response.status_int != 200:
        raise AssertionError
    if 'I\'m Feeling Lucky' not in response.body:
        raise AssertionError


@mock.patch('rpc.urlfetch')
def test_url_fetch_rpc_error(urlfetch_mock, app):
    urlfetch_mock.DownloadError = urlfetch.DownloadError
    get_result_mock = mock.Mock(
        side_effect=urlfetch.DownloadError())
    urlfetch_mock.create_rpc = mock.Mock(
        return_value=mock.Mock(get_result=get_result_mock))
    response = app.get('/', status=500)
    if 'Error fetching URL' not in response.body:
        raise AssertionError


@mock.patch('rpc.urlfetch')
def test_url_fetch_http_error(urlfetch_mock, app):
    get_result_mock = mock.Mock(
        return_value=mock.Mock(
            status_code=404,
            content='Not Found'))
    urlfetch_mock.create_rpc = mock.Mock(
        return_value=mock.Mock(get_result=get_result_mock))
    response = app.get('/', status=404)
    if '404' not in response.body:
        raise AssertionError


@mock.patch('rpc.urlfetch')
def test_url_post(urlfetch_mock, app):
    get_result_mock = mock.Mock(
        return_value=mock.Mock(
            status_code=200,
            content='I\'m Feeling Lucky'))
    urlfetch_mock.create_rpc = mock.Mock(
        return_value=mock.Mock(get_result=get_result_mock))

    rpc_mock = mock.Mock()
    urlfetch_mock.create_rpc.return_value = rpc_mock

    app.get('/callback')
    rpc_mock.wait.assert_called_with()
