# Copyright 2023 Google, LLC.
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
import unittest

from google.events.cloud.audit import LogEntryData, AuditLog, AuthenticationInfo

from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary

import main


ce_attributes = {
    "id": str(uuid4),
    "type": "com.pytest.sample.event",
    "source": "<my-test-source>",
    "specversion": "1.0",
}


@pytest.fixture
def client(request):
    main.app.testing = True
    return main.app.test_client()


def test_endpoint(client, capsys):
    logentry = LogEntryData(
        proto_payload=AuditLog(
            service_name="storage.googleapis.com",
            resource_name="my-bucket/my-file.txt",
            authentication_info=AuthenticationInfo(principal_email="user@example.com"),
        )
    )
    event = CloudEvent(ce_attributes, LogEntryData.to_dict(logentry))
    headers, body = to_binary(event)

    r = client.post("/", headers=headers, data=body)
    assert (
        "my-bucket/my-file.txt updated by user@example.com"
        in r.get_data(as_text=True)
    )
