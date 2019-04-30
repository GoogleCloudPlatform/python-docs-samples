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

from googleapiclient.http import HttpMockSequence
import httplib2
import mock
import pytest
import webtest

import main


class HttpMockSequenceWithCredentials(HttpMockSequence):
    def add_credentials(self, *args):
        pass


@pytest.fixture
def app():
    return webtest.TestApp(main.app)


def test_get(app):
    response = app.get('/')
    assert response.status_int == 200


def test_post(app):
    http = HttpMockSequenceWithCredentials([
        ({'status': '200'}, '')])
    patch_http = mock.patch.object(httplib2, 'Http', lambda: http)

    with patch_http:
        response = app.post('/', {
            'recipient': 'jonwayne@google.com',
            'submit': 'Send simple email'})

        assert response.status_int == 200

    http = HttpMockSequenceWithCredentials([
        ({'status': '200'}, '')])

    with patch_http:
        response = app.post('/', {
            'recipient': 'jonwayne@google.com',
            'submit': 'Send complex email'})

        assert response.status_int == 200

    http = HttpMockSequenceWithCredentials([
        ({'status': '500'}, 'Test error')])

    with patch_http, pytest.raises(Exception):
        app.post('/', {
            'recipient': 'jonwayne@google.com',
            'submit': 'Send simple email'})
