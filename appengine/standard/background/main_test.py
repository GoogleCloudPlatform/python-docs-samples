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

import os

from mock import patch
import pytest
import webtest

import main

PROJECT = os.environ['GCLOUD_PROJECT']


@pytest.fixture
def app(testbed):
    main.PROJECTID = PROJECT
    return webtest.TestApp(main.app)


@patch("main.background_thread")
def test_background(thread, app):
    app.get('/dog')
    response = app.get('/')
    assert response.status_int == 200
    assert response.body == 'Dog'
    app.get('/cat')
    # no stub for system so manually set
    main.val = 'Cat'
    response = app.get('/')
    assert response.status_int == 200
    assert response.body == 'Cat'


@patch("main.background_thread")
def test_background_auto_start(thread, app):
    app.get('/dog')
    response = app.get('/')
    assert response.status_int == 200
    assert response.body == 'Dog'
    app.get('/cat?auto=True')
    # no stub for system so manually set
    main.val = 'Cat'
    response = app.get('/')
    assert response.status_int == 200
    assert response.body == 'Cat'
