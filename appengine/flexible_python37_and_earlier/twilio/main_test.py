# Copyright 2016 Google LLC.
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
    monkeypatch.setenv('TWILIO_ACCOUNT_SID', 'sid123')
    monkeypatch.setenv('TWILIO_AUTH_TOKEN', 'auth123')
    monkeypatch.setenv('TWILIO_NUMBER', '0123456789')

    import main

    main.app.testing = True
    return main.app.test_client()


def test_receive_call(app):
    r = app.post('/call/receive')
    assert 'Hello from Twilio!' in r.data.decode('utf-8')


@responses.activate
def test_send_sms(app, monkeypatch):
    sample_response = {
        "sid": "sid",
        "date_created": "Wed, 20 Dec 2017 19:32:14 +0000",
        "date_updated": "Wed, 20 Dec 2017 19:32:14 +0000",
        "date_sent": None,
        "account_sid": "account_sid",
        "to": "+1234567890",
        "from": "+9876543210",
        "messaging_service_sid": None,
        "body": "Hello from Twilio!",
        "status": "queued",
        "num_segments": "1",
        "num_media": "0",
        "direction": "outbound-api",
        "api_version": "2010-04-01",
        "price": None,
        "price_unit": "USD",
        "error_code": None,
        "error_message": None,
        "uri": "/2010-04-01/Accounts/sample.json",
        "subresource_uris": {
            "media": "/2010-04-01/Accounts/sample/Media.json"
        }
    }
    responses.add(responses.POST, re.compile('.*'),
                  json=sample_response, status=200)

    r = app.get('/sms/send')
    assert r.status_code == 400

    r = app.get('/sms/send?to=5558675309')
    assert r.status_code == 200


def test_receive_sms(app):
    r = app.post('/sms/receive', data={
        'From': '5558675309', 'Body': 'Jenny, I got your number.'})
    assert r.status_code == 200
    assert 'Jenny, I got your number' in r.data.decode('utf-8')
