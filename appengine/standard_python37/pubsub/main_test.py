# Copyright 2018 Google, LLC.
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

import base64
import calendar
import datetime
import json
import os

from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
from google.oauth2 import id_token

import mock
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
def token_factory(signer):
    now = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
    payload = {
        'aud': 'https://example.com/_ah/push-handlers/receive_messages?token=1234abc',
        'azp': '1234567890',
        'email': 'pubsub@example.iam.gserviceaccount.com',
        'email_verified': True,
        'exp': now,
        'iat': now + 300,
        'iss': 'https://accounts.google.com',
        'sub': '1234567890'
    }
    header = {
        'alg': 'RS256',
        'kid': signer.key_id,
        'typ': 'JWT'
    }
    return jwt.encode(signer, payload, header=header)


def test_index(client):
    r = client.get('/')
    assert r.status_code == 200


def test_post_index(client):
    r = client.post('/', data={'payload': 'Test payload'})
    assert r.status_code == 200


def _verify_oauth2_token_patch():
    real_verify = jwt.decode

    def mock_verify():
        real_verify(factory, certs=PUBLIC_CERT_BYTES, verify=True)

    return mock.patch('id_token.verify_oauth2_token', new=mock_verify)


def test_push_endpoint(client):
    url = '/_ah/push-handlers/receive_messages?token=' + \
        os.environ['PUBSUB_VERIFICATION_TOKEN']

    r = None
    with _verify_oauth2_token_patch():
        r = client.post(
            url,
            data=json.dumps({
                "message": {
                    "data": base64.b64encode(
                        u'Test message'.encode('utf-8')
                    ).decode('utf-8')
                }
            }),
            header=json.dumps({
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token_factory()
            })
        )

    assert r.status_code == 200

    # Make sure the message is visible on the home page.
    r = client.get('/')
    assert r.status_code == 200
    assert 'Test message' in r.data.decode('utf-8')


def test_push_endpoint_errors(client):
    # no token
    r = client.post('/_ah/push-handlers/receive_messages')
    assert r.status_code == 400

    # invalid token
    r = client.post('/_ah/push-handlers/receive_messages?token=bad')
    assert r.status_code == 400
