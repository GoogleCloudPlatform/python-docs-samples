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

import pytest
import uuid

import google.auth


import http_queues

def test_httpq_lifecycle() -> None:
    # Use the default project and a random name for the test queue
    _, project = google.auth.default()
    name = uuid.uuid4().hex

    q = http_queues.create_http_queue(project, "us-central1", name, "http://example.com/")
    assert q is not None
    assert q.http_target.uri_override is not None
    assert q.http_target.uri_override.host == "example.com"
    assert q.http_target.uri_override.scheme == 1

    q = http_queues.update_http_queue(q, uri="https://example.com/somepath")
    assert q.http_target.uri_override.scheme != 1
    assert q.http_target.uri_override.path_override.path == "/somepath"

    q = http_queues.update_http_queue(q, max_per_second=5.0, max_attempts=2)
    assert q.rate_limits is not None
    assert q.rate_limits.max_dispatches_per_second == 5.0
    assert q.retry_config.max_attempts == 2

    q2 = http_queues.get_http_queue(project, "us-central1", name)
    assert q2 is not None
    assert q2 == q

    result = http_queues.send_task_to_http_queue(q, body="something")
    assert result < 400

    http_queues.delete_http_queue(q)

    with pytest.raises(Exception) as exc_info:
        q3 = http_queues.get_http_queue(project, "us-central1", name)
    assert exc_info.typename == "NotFound"
