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

import webtest

import taskqueue


def test_taskqueue(testbed, run_tasks):
    app = webtest.TestApp(taskqueue.app)

    response = app.get('/taskqueue')
    assert response.status_int == 200
    assert 'Global: 0' in response.body

    run_tasks(app)

    response = app.get('/taskqueue')
    assert response.status_int == 200
    assert 'Global: 1' in response.body

    response = app.get('/taskqueue/a')
    assert response.status_int == 200
    assert 'a: 0' in response.body

    run_tasks(app)

    response = app.get('/taskqueue/a')
    assert response.status_int == 200
    assert 'a: 1' in response.body
