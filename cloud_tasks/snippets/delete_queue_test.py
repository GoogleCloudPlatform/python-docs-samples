# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from google.api_core import exceptions
from google.cloud import tasks_v2
import pytest

import delete_queue

TEST_PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TEST_LOCATION = os.getenv("TEST_QUEUE_LOCATION", "us-central1")
TEST_QUEUE_NAME = f"my-queue-{uuid.uuid4().hex}"


@pytest.fixture()
def test_queue():
    client = tasks_v2.CloudTasksClient()
    parent = f"projects/{TEST_PROJECT_ID}/locations/{TEST_LOCATION}"
    queue = {
        # The fully qualified path to the queue
        "name": client.queue_path(TEST_PROJECT_ID, TEST_LOCATION, TEST_QUEUE_NAME),
    }
    q = client.create_queue(request={"parent": parent, "queue": queue})

    yield q

    try:
        # Attempt to delete the queue in case the sample failed.
        client.delete_queue(request={"name": q.name})
    except exceptions.NotFound:
        # The queue was already successfully deleted.
        print("Queue already deleted successfully")


def test_delete_queue(capsys, test_queue):
    delete_queue.delete_queue(TEST_PROJECT_ID, TEST_QUEUE_NAME, TEST_LOCATION)
    out, _ = capsys.readouterr()
    assert "Deleted queue" in out
