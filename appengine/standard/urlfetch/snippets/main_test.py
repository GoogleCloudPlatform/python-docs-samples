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
def app(testbed):
    return webtest.TestApp(main.app)


def test_url_lib(app):
    response = app.get('/')
    assert 'Google' in response.body


def test_url_fetch(app):
    response = app.get('/url_fetch')
    assert 'Google' in response.body


@mock.patch("main.urlfetch")
def test_url_post(urlfetch_mock, app):
    urlfetch_mock.fetch = mock.Mock(
        return_value=mock.Mock(content='Albert',
                               status_code=200))
    response = app.get('/url_post')
    assert 'Albert' in response.body
