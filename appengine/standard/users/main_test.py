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

import main


def test_index(testbed, login):
    app = webtest.TestApp(main.app)

    response = app.get('/')
    assert 'Login' in response.body

    login()
    response = app.get('/')
    assert 'Logout' in response.body
    assert 'user@example.com' in response.body


def test_admin(testbed, login):
    app = webtest.TestApp(main.app)

    response = app.get('/admin')
    assert 'You are not logged in' in response.body

    login()
    response = app.get('/admin')
    assert 'You are not an administrator' in response.body

    login(is_admin=True)
    response = app.get('/admin')
    assert 'You are an administrator' in response.body
