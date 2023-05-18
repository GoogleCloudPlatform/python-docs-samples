# Copyright 2019 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is for testing purposes only. You SHOULD NOT include it
# or the PEM files when deploying your app.

import base64
import calendar
import datetime
import json
import os

from google.auth import crypt
from google.auth import jwt
from google.oauth2 import id_token
import pytest

import main


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

with open(os.path.join(DATA_DIR, 'privatekey.pem'), 'rb') as fh:
    PRIVATE_KEY_BYTES = fh.read()

with open(os.path.join(DATA_DIR, 'public_cert.pem'), 'rb') as fh:
    PUBLIC_CERT_BYTES = fh.read()


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


@pytest.fixture
def signer():
    return crypt.RSASigner.from_string(PRIVATE_KEY_BYTES, '1')


@pytest.fixture
def fake_token(signer):
    now = calendar.timegm(datetime.datetime.now(tz=datetime.timezone.utc).utctimetuple())
    payload = {
        'aud': 'example.com',
        'azp': '1234567890',
        'email': 'pubsub@example.iam.gserviceaccount.com',
        'email_verified': True,
        'iat': now,
        'exp': now + 3600,
        'iss': 'https://accounts.google.com',
        'sub': '1234567890'
    }
    header = {
        'alg': 'RS256',
        'kid': signer.key_id,
        'typ': 'JWT'
    }
    yield jwt.encode(signer, payload, header=header)


def _verify_mocked_oauth2_token(token, request, audience):
    claims = jwt.decode(token, certs=PUBLIC_CERT_BYTES, verify=True)
    return claims


def test_index(client):
    r = client.get('/')
    assert r.status_code == 200


def test_post_index(client):
    r = client.post('/', data={'payload': 'Test payload'})
    assert r.status_code == 200


def test_push_endpoint(monkeypatch, client, fake_token):
    monkeypatch.setattr(id_token, 'verify_oauth2_token',
                        _verify_mocked_oauth2_token)

    url = '/push-handlers/receive_messages?token=' + \
        os.environ['PUBSUB_VERIFICATION_TOKEN']

    r = client.post(
        url,
        data=json.dumps({
            "message": {
                "data": base64.b64encode(
                    b'Test message'
                ).decode('utf-8')
            }
        }),
        headers=dict(
            Authorization="Bearer " + fake_token.decode('utf-8')
        )
    )
    assert r.status_code == 200

    # Make sure the message is visible on the home page.
    r = client.get('/')
    assert r.status_code == 200
    assert 'Test message' in r.data.decode('utf-8')


def test_push_endpoint_errors(client):
    # no token
    r = client.post('/push-handlers/receive_messages')
    assert r.status_code == 400

    # invalid token
    r = client.post('/push-handlers/receive_messages?token=bad')
    assert r.status_code == 400
