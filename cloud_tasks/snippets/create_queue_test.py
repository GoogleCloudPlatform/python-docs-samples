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

from google.cloud import tasks_v2
import pytest

import create_queue

TEST_PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TEST_LOCATION = os.getenv("TEST_QUEUE_LOCATION", "us-central1")
TEST_QUEUE_NAME = f"my-queue-{uuid.uuid4().hex}"


@pytest.fixture()
def test_queue():
    client = tasks_v2.CloudTasksClient()
    q = create_queue.create_queue(TEST_PROJECT_ID, TEST_QUEUE_NAME, TEST_LOCATION)

    yield q

    client.delete_queue(request={"name": q.name})


def test_create_queue(capsys, test_queue):
    out, _ = capsys.readouterr()
    assert "Created queue" in out
