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
import pytest
import webtest

import main


@pytest.fixture
def app():
    return webtest.TestApp(main.app)


@mock.patch("main.modules")
def test_get_module_info(modules_mock, app):
    modules_mock.get_current_module_name.return_value = "default"
    modules_mock.get_current_instance_id.return_value = 1
    response = app.get('/')
    assert response.status_int == 200
    results = response.body.split('&')
    assert results[0].split('=')[1] == 'default'
    assert results[1].split('=')[1] == '1'


@mock.patch("main.modules")
@mock.patch("urllib2.urlopen")
def test_get_backend(url_open_mock, modules_mock, app):
    url_read_mock = mock.Mock(read=mock.Mock(return_value='hello world'))
    url_open_mock.return_value = url_read_mock
    response = app.get('/access_backend')

    assert response.status_int == 200
    assert response.body == 'Got response hello world'
