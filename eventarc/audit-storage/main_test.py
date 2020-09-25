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
import copy

from uuid import uuid4

import pytest

import main


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


def test_endpoint(client, capsys):
    test_headers = copy.copy(binary_headers)
    test_headers['Ce-Subject'] = 'test-subject'

    r = client.post('/', headers=test_headers)
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    assert f"Detected change in GCS bucket: {test_headers['Ce-Subject']}" in out


def test_missing_subject(client, capsys):
    r = client.post('/', headers=binary_headers)
    assert r.status_code == 400

    out, _ = capsys.readouterr()
    assert 'Bad Request: expected header ce-subject' in out


def test_missing_required_fields(client, capsys):
    for field in binary_headers:
        test_headers = copy.copy(binary_headers)
        test_headers.pop(field)

        r = client.post('/', headers=test_headers)
        assert r.status_code == 400

        out, _ = capsys.readouterr()
        assert 'MissingRequiredFields' in out
