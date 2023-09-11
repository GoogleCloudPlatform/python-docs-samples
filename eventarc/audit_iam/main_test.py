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
}


@pytest.fixture
def client(request):
    main.app.testing = True
    return main.app.test_client()


def test_endpoint(client, capsys):
    rawobj = {
        "protoPayload": {
            "@type": "....",
            "service_name": "iam.googleapis.com",
            "status": {
                "code": 0,
            },
            "authenticationInfo": {"principalEmail": "user@example.com"},
            "request": {
                "name": "projects/-/serviceAccounts/service-account@my-project.iam.gserviceaccount.com"
            },
            "response": {
                "name": "projects/my-project/serviceAccounts/service-account@my-project.iam.gserviceaccount.com/keys/deadbeef"
            },
        },
    }
    event = CloudEvent(ce_attributes, rawobj)
    headers, body = to_binary(event)

    r = client.post("/", headers=headers, data=body)
    assert (
        "New Service Account Key created for projects/-/serviceAccounts/service-account@"
        in r.text
    )

    assert "by user@example.com" in r.text
