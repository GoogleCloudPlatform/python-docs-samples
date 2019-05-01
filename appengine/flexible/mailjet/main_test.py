# Copyright 2016 Google Inc. All Rights Reserved.
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

import re

import pytest
import responses


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('MAILJET_API_KEY', 'apikey')
    monkeypatch.setenv('MAILJET_API_SECRET', 'apisecret')
    monkeypatch.setenv('MAILJET_SENDER', 'sender')

    import main

    main.app.testing = True
    return main.app.test_client()


def test_index(app):
    r = app.get('/')
    assert r.status_code == 200


@responses.activate
def test_send_email(app):
    responses.add(
        responses.POST,
        re.compile(r'.*'),
        body='{"test": "message"}',
        content_type='application/json')

    r = app.post('/send/email', data={'to': 'user@example.com'})

    assert r.status_code == 200
    assert 'test' in r.data.decode('utf-8')

    assert len(responses.calls) == 1
    request_body = responses.calls[0].request.body
    assert 'user@example.com' in request_body
