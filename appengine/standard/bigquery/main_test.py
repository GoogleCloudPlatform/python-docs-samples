# Copyright 2015 Google Inc. All rights reserved.
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

import os
import re

from googleapiclient.http import HttpMock
import mock
import pytest
import webtest

import main

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
PROJECT = os.environ['GCLOUD_PROJECT']


@pytest.fixture
def app(testbed):
    main.PROJECTID = PROJECT
    return webtest.TestApp(main.app)


def test_anonymous(app):
    response = app.get('/')

    # Should redirect to login
    assert response.status_int == 302
    assert re.search(r'.*accounts.*Login.*', response.headers['Location'])


def test_loggedin(app, login):
    login()

    response = app.get('/')

    # Should redirect to oauth2
    assert response.status_int == 302
    assert re.search(r'.*oauth2.*', response.headers['Location'])


def test_oauthed(app, login):
    login()

    mock_http = HttpMock(
        os.path.join(RESOURCES, 'datasets-list.json'),
        {'status': '200'})

    with mock.patch.object(main.decorator, 'http', return_value=mock_http):
        with mock.patch.object(
                main.decorator, 'has_credentials', return_value=True):
            response = app.get('/')

    # Should make the api call
    assert response.status_int == 200
    assert re.search(
        re.compile(r'.*datasets.*datasetReference.*etag.*', re.DOTALL),
        response.body)
