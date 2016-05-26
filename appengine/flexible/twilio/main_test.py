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

import json

from googleapiclient.http import HttpMockSequence
import httplib2
import pytest


class HttpMockSequenceWithCredentials(HttpMockSequence):
    def add_credentials(self, *args):
        pass


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('TWILIO_ACCOUNT_SID', 'sid123')
    monkeypatch.setenv('TWILIO_AUTH_TOKEN', 'auth123')
    monkeypatch.setenv('TWILIO_NUMBER', '0123456789')

    import main

    main.app.testing = True
    return main.app.test_client()


def test_receive_call(app):
    r = app.post('/call/receive')
    assert 'Hello from Twilio!' in r.data.decode('utf-8')


def test_send_sms(app, monkeypatch):
    httpmock = HttpMockSequenceWithCredentials([
        ({'status': '200'}, json.dumps({
            'sid': 'sid123'
        }))
    ])

    def mock_http_ctor(*args, **kwargs):
        return httpmock

    monkeypatch.setattr(httplib2, 'Http', mock_http_ctor)

    r = app.get('/sms/send')
    assert r.status_code == 400

    r = app.get('/sms/send?to=5558675309')
    assert r.status_code == 200


def test_receive_sms(app):
    r = app.post('/sms/receive', data={
        'From': '5558675309', 'Body': 'Jenny, I got your number.'})
    assert r.status_code == 200
    assert 'Jenny, I got your number' in r.data.decode('utf-8')
