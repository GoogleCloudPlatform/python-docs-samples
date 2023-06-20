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

from cloudevents.conversion import to_binary
from cloudevents.http import CloudEvent

import pytest

import main


ce_attributes = {
    "id": str(uuid4),
    "type": "com.pytest.sample.event",
    "source": "<my-test-source>",
    "specversion": "1.0",
    "subject": "test-bucket",
}


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_endpoint(client):
    event = CloudEvent(ce_attributes, dict())

    headers, body = to_binary(event)

    r = client.post("/", headers=headers, data=body)
    assert r.status_code == 200
    assert "Detected change in Cloud Storage bucket: test-bucket" in r.text
