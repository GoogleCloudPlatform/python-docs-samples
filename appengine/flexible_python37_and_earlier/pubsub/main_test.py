# Copyright 2015 Google LLC.
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

import base64
import json
import os

import pytest

import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_index(client):
    r = client.get('/')
    assert r.status_code == 200


def test_post_index(client):
    r = client.post('/', data={'payload': 'Test payload'})
    assert r.status_code == 200


def test_push_endpoint(client):
    url = '/pubsub/push?token=' + os.environ['PUBSUB_VERIFICATION_TOKEN']

    r = client.post(
        url,
        data=json.dumps({
            "message": {
                "data": base64.b64encode(
                    u'Test message'.encode('utf-8')
                ).decode('utf-8')
            }
        })
    )

    assert r.status_code == 200

    # Make sure the message is visible on the home page.
    r = client.get('/')
    assert r.status_code == 200
    assert 'Test message' in r.data.decode('utf-8')


def test_push_endpoint_errors(client):
    # no token
    r = client.post('/pubsub/push')
    assert r.status_code == 400

    # invalid token
    r = client.post('/pubsub/push?token=bad')
    assert r.status_code == 400
