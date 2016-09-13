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

from google.appengine.ext import deferred
import webtest

import main


def test_app(testbed):
    app = webtest.TestApp(main.app)
    response = app.get('/')
    assert response.status_int == 200


def test_add_entities(testbed):
    app = webtest.TestApp(main.app)
    response = app.post('/add_entities')
    assert response.status_int == 200
    response = app.get('/')
    assert response.status_int == 200
    assert 'Author: Bob' in response.body
    assert 'Name: Sunrise' in response.body
    assert 'Author: Alice' in response.body
    assert 'Name: Sunset' in response.body


def test_update_schema(testbed, run_tasks):
    app = webtest.TestApp(main.app)
    testbed.activate()
    taskqueue_stub = testbed.get_stub('taskqueue')
    response = app.post('/add_entities')
    response = app.get('/')
    response = app.post('/update_schema')
    assert response.status_int == 200
    tasks = taskqueue_stub.get_filtered_tasks()
    deferred.run(tasks[0].payload)
    response = app.get('/')
    assert response.status_int == 200
    assert 'Votes: 1' in response.body
    assert 'Average Rating: 5.0' in response.body
