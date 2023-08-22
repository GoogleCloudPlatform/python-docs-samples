#!/usr/bin/env python
#
# Copyright 2022 Google, Inc.
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

import os
from typing import Generator
import uuid

from google.api_core.retry import Retry
from google.cloud import tasks_v2
import pytest

import create_http_task

TEST_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_LOCATION = os.getenv("TEST_QUEUE_LOCATION", "us-central1")
TEST_QUEUE_ID = f"my-queue-{uuid.uuid4().hex}"


@pytest.fixture()
def test_queue() -> Generator[tasks_v2.Queue, None, None]:
    client = tasks_v2.CloudTasksClient()
    queue = client.create_queue(
        tasks_v2.CreateQueueRequest(
            parent=client.common_location_path(TEST_PROJECT_ID, TEST_LOCATION),
            queue=tasks_v2.Queue(
                name=client.queue_path(TEST_PROJECT_ID, TEST_LOCATION, TEST_QUEUE_ID)
            ),
        )
    )

    yield queue
    client.delete_queue(request={"name": queue.name})


@Retry()
def test_create_http_task(test_queue: tasks_v2.Queue) -> None:
    task = create_http_task.create_http_task(
        TEST_PROJECT_ID,
        TEST_LOCATION,
        TEST_QUEUE_ID,
        "https://example.com/task_handler",
        json_payload={"greeting": "hola"},
        scheduled_seconds_from_now=180,
        task_id=uuid.uuid4().hex,
        deadline_in_seconds=900,
    )
    assert task.name.startswith(test_queue.name)
    assert task.http_request.url == "https://example.com/task_handler"
