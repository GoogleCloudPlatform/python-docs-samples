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

# NOTE:
# These tests are unit tests that mock Pub/Sub.

import base64
from uuid import uuid4

import pytest

import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_empty_payload(client):
    r = client.post('/', json='')
    assert r.status_code == 400


def test_invalid_payload(client):
    r = client.post('/', json={'nomessage': 'invalid'})
    assert r.status_code == 400


def test_invalid_mimetype(client):
    r = client.post('/', json="{ message: true }")
    assert r.status_code == 400


def test_minimally_valid_message(client, capsys):
    r = client.post('/', json={'message': True})
    assert r.status_code == 204

    out, _ = capsys.readouterr()
    assert 'Hello World!' in out


def test_populated_message(client, capsys):
    name = str(uuid4())
    data = base64.b64encode(name.encode()).decode()

    r = client.post('/', json={'message': {'data': data}})
    assert r.status_code == 204

    out, _ = capsys.readouterr()
    assert f'Hello {name}!' in out
