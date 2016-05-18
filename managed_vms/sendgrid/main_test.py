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

import main

import mock
import pytest


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('SENDGRID_API_KEY', 'apikey')
    monkeypatch.setenv('SENDGRID_SENDER', 'sender@example.com')

    import main

    main.app.testing = True
    return main.app.test_client()


def test_get(app):
    r = app.get('/')
    assert r.status_code == 200


@mock.patch.object(
    main.sendgrid.SendGridClient, 'send', return_value=(200, "OK"))
def test_post(send_mock, app):
    r = app.post('/send/email', data={
        'to': 'user@example.com'
    })
    assert r.status_code == 200
    assert send_mock.called
