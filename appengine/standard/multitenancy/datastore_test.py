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

import datastore


def test_datastore(testbed):
    app = webtest.TestApp(datastore.app)

    response = app.get('/datastore')
    if response.status_int != 200:
        raise AssertionError
    if 'Global: 1' not in response.body:
        raise AssertionError

    response = app.get('/datastore/a')
    if response.status_int != 200:
        raise AssertionError
    if 'Global: 2' not in response.body:
        raise AssertionError
    if 'a: 1' not in response.body:
        raise AssertionError

    response = app.get('/datastore/b')
    if response.status_int != 200:
        raise AssertionError
    if 'Global: 3' not in response.body:
        raise AssertionError
    if 'b: 1' not in response.body:
        raise AssertionError
