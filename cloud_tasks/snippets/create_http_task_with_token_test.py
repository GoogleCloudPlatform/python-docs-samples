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
import uuid

from google.cloud import tasks_v2
import pytest

import create_http_task_with_token

TEST_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_LOCATION = os.getenv("TEST_QUEUE_LOCATION", "us-central1")
TEST_QUEUE_NAME = f"my-queue-{uuid.uuid4().hex}"
TEST_SERVICE_ACCOUNT = (
    "test-run-invoker@python-docs-samples-tests.iam.gserviceaccount.com"
)


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

    client.delete_queue(request={"name": q.name})


def test_create_http_task_with_token(test_queue):
    url = "https://example.com/task_handler"
    result = create_http_task_with_token.create_http_task(
        TEST_PROJECT_ID, TEST_QUEUE_NAME, TEST_LOCATION, url, TEST_SERVICE_ACCOUNT
    )
    assert TEST_QUEUE_NAME in result.name
