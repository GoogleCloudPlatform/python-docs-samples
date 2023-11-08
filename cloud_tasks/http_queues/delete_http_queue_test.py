# Copyright 2023 Google LLC
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

import uuid

from google.api_core.exceptions import NotFound
import google.auth

# HTTP Queues are currently in public beta
from google.cloud import tasks_v2beta3 as tasks

import pytest

import delete_http_queue


HOST = "example.com"
LOCATION = "us-central1"


@pytest.fixture
def q():
    # Use the default project and a random name for the test queue
    _, project = google.auth.default()
    name = "tests-tasks-" + uuid.uuid4().hex

    http_target = {
        "uri_override": {
            "host": HOST,
            "uri_override_enforce_mode": 2,  # ALWAYS use this endpoint
        }
    }

    # Use the client to send a CreateQueueRequest.
    client = tasks.CloudTasksClient()
    queue = client.create_queue(
        tasks.CreateQueueRequest(
            parent=client.common_location_path(project, LOCATION),
            queue={
                "name": f"projects/{project}/locations/{LOCATION}/queues/{name}",
                "http_target": http_target,
            },
        )
    )

    yield queue

    try:
        client.delete_queue(name=queue.name)
    except Exception as e:
        if type(e) == NotFound:  # It's still gone, anyway, so it's fine
            pass
        else:
            print(f"Tried my best to clean up, but could not: {e}")


def test_delete_http_queue(q) -> None:
    name = q.name
    delete_http_queue.delete_http_queue(q)

    client = tasks.CloudTasksClient()
    with pytest.raises(Exception) as exc_info:
        client.get_queue(name=name)
    assert exc_info.typename == "NotFound"
