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

from google.api_core.retry import Retry
from google.cloud import tasks_v2

import create_queue

TEST_PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TEST_LOCATION = os.getenv("TEST_QUEUE_LOCATION", "us-central1")
TEST_QUEUE_ID = f"my-queue-{uuid.uuid4().hex}"


@Retry()
def test_create_queue() -> None:
    client = tasks_v2.CloudTasksClient()

    queue = create_queue.create_queue(TEST_PROJECT_ID, TEST_LOCATION, TEST_QUEUE_ID)
    assert queue.name == client.queue_path(
        TEST_PROJECT_ID, TEST_LOCATION, TEST_QUEUE_ID
    )

    client.delete_queue(tasks_v2.DeleteQueueRequest(name=queue.name))
