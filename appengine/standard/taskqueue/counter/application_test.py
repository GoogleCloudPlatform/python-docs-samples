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

import webtest

import application
import worker


def test_all(testbed, run_tasks):
    test_app = webtest.TestApp(application.app)
    test_worker = webtest.TestApp(worker.app)

    response = test_app.get('/')
    assert '0' in response.body

    test_app.post('/enqueue', {'amount': 5})
    run_tasks(test_worker)

    response = test_app.get('/')
    assert '5' in response.body
