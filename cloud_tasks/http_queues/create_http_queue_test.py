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

import google.auth

# HTTP Queues are currently in public beta
from google.cloud import tasks_v2beta3 as tasks

import create_http_queue


def test_create() -> None:
    # Use the default project and a random name for the test queue
    _, project = google.auth.default()
    name = "tests-tasks-" + uuid.uuid4().hex

    q = create_http_queue.create_http_queue(
        project, "us-central1", name, "http://example.com/"
    )
    assert q is not None
    assert q.http_target.uri_override is not None
    assert q.http_target.uri_override.host == "example.com"
    assert q.http_target.uri_override.scheme == 1

    try:
        client = tasks.Client()
        client.delete_queue(name=q.name)
    except Exception as e:
        print(f"Tried my best to clean up, but could not: {e}")
