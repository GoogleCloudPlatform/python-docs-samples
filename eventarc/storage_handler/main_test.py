# Copyright 2023 Google LLC.
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

# [START eventarc_testing_cloudevent]
from uuid import uuid4

from cloudevents.conversion import to_binary
from cloudevents.http import CloudEvent

from google.events.cloud.storage import StorageObjectData

import pytest

import main


ce_attributes = {
    "id": str(uuid4),
    "type": "com.pytest.sample.event",
    "source": "<my-test-source>",
    "specversion": "1.0",
}


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_endpoint(client):
    storagedata = StorageObjectData(bucket="test-bucket", name="my-file.txt")
    event = CloudEvent(ce_attributes, StorageObjectData.to_dict(storagedata))
    headers, body = to_binary(event)

    r = client.post("/", headers=headers, data=body)
    assert r.status_code == 200
    assert "Cloud Storage object changed: test-bucket/my-file.txt" in r.text


# [END eventarc_testing_cloudevent]


def test_invalid_data(client):
    event = CloudEvent(ce_attributes, {"an_unknown_field": "some_value"})
    headers, body = to_binary(event)

    r = client.post("/", headers=headers, data=body)
    assert r.status_code == 400
