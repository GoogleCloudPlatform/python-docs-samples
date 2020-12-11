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

from google.appengine.runtime import DeadlineExceededError
import mock
import webtest

import main


def test_timer(testbed):
    app = webtest.TestApp(main.app)

    with mock.patch('main.time.sleep') as sleep_mock:
        sleep_mock.side_effect = DeadlineExceededError()
        app.get('/timer', status=500)
        if not sleep_mock.called:
            raise AssertionError


def test_environment(testbed):
    app = webtest.TestApp(main.app)
    response = app.get('/environment')
    if response.headers['Content-Type'] != 'text/plain':
        raise AssertionError
    if not response.body:
        raise AssertionError


def test_request_id(testbed):
    app = webtest.TestApp(main.app)
    os.environ['REQUEST_LOG_ID'] = '1234'
    response = app.get('/requestid')
    if response.headers['Content-Type'] != 'text/plain':
        raise AssertionError
    if '1234' not in response.body:
        raise AssertionError
