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
TEST_QUEUE_ID = f"my-queue-{uuid.uuid4().hex}"


def test_delete_queue() -> None:
    client = tasks_v2.CloudTasksClient()

    client.create_queue(
        tasks_v2.CreateQueueRequest(
            parent=client.common_location_path(TEST_PROJECT_ID, TEST_LOCATION),
            queue=tasks_v2.Queue(
                name=client.queue_path(TEST_PROJECT_ID, TEST_LOCATION, TEST_QUEUE_ID)
            ),
        )
    )

    # Deleting an existant queue succeeds
    delete_queue.delete_queue(TEST_PROJECT_ID, TEST_LOCATION, TEST_QUEUE_ID)

    # Deleting a non-existant queue fails with a not found error
    with pytest.raises(exceptions.NotFound):
        delete_queue.delete_queue(TEST_PROJECT_ID, TEST_LOCATION, TEST_QUEUE_ID)
