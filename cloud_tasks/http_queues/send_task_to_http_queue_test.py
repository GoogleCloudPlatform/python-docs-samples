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

import json
import subprocess
import uuid

import google.auth

# HTTP Queues are currently in public beta
from google.cloud import tasks_v2beta3 as tasks

import pytest

import send_task_to_http_queue


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
        print(f"Tried my best to clean up, but could not: {e}")


def get_access_token():
    output = subprocess.run(
        "gcloud auth application-default print-access-token --quiet --format=json",
        capture_output=True,
        shell=True,
        check=True,
    )
    entries = json.loads(output.stdout)
    return entries["token"]


def test_send_task_to_http_queue(q) -> None:
    token = get_access_token()
    result = send_task_to_http_queue.send_task_to_http_queue(
        q, body="something", token=token
    )
    assert result < 400
