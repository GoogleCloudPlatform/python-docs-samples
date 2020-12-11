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

from google.appengine.ext import deferred
import pytest
import webtest

import main
import models_v1
import models_v2


@pytest.fixture
def app(testbed):
    yield webtest.TestApp(main.app)


def test_app(app):
    response = app.get('/')
    if response.status_int != 200:
        raise AssertionError


def test_add_entities(app):
    response = app.post('/add_entities')
    if response.status_int != 200:
        raise AssertionError
    response = app.get('/')
    if response.status_int != 200:
        raise AssertionError
    if 'Author: Bob' not in response.body:
        raise AssertionError
    if 'Name: Sunrise' not in response.body:
        raise AssertionError
    if 'Author: Alice' not in response.body:
        raise AssertionError
    if 'Name: Sunset' not in response.body:
        raise AssertionError


def test_update_schema(app, testbed):
    reload(models_v1)
    test_model = models_v1.Picture(author='Test', name='Test')
    test_model.put()

    response = app.post('/update_schema')
    if response.status_int != 200:
        raise AssertionError

    # Run the queued task.
    tasks = testbed.taskqueue_stub.get_filtered_tasks()
    if len(tasks) != 1:
        raise AssertionError
    deferred.run(tasks[0].payload)

    # Check the updated items
    reload(models_v2)
    updated_model = test_model.key.get()
    if updated_model.num_votes != 1:
        raise AssertionError
    if updated_model.avg_rating != 5.0:
        raise AssertionError
