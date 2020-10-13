# Copyright 2020 Google, LLC.
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
from uuid import uuid4

import main

import pytest


binary_headers = {
    "ce-id": str(uuid4),
    "ce-type": "com.pytest.sample.event",
    "ce-source": "<my-test-source>",
    "ce-specversion": "1.0"
}


@pytest.fixture
def client():

    main.app.testing = True
    return main.app.test_client()


def test_relay(client, capsys):

    r = client.post('/', json={'message': {'data': 'Hello'}}, headers=binary_headers)
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    ce_id = binary_headers['ce-id']

    # Ensure the output prints HTTP headers and body
    assert 'Event received!' in out
    assert ce_id in out
    assert "{'message': {'data': 'Hello'}}" in out
