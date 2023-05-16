# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

import google.auth
from google.cloud import storage
import pytest

import async_api


# TODO(developer): Replace the variables in the file before use.
# A sample request model can be found at resources/async_request_model.json.
TEST_UUID = uuid.uuid4()
BUCKET = f"optimization-ai-{TEST_UUID}"
OUTPUT_PREFIX = f"code_snippets_test_output_{TEST_UUID}"
INPUT_URI = "gs://cloud-samples-data/optimization-ai/async_request_model.json"
BATCH_OUTPUT_URI_PREFIX = f"gs://{BUCKET}/{OUTPUT_PREFIX}/"


@pytest.fixture(autouse=True)
def setup_teardown() -> None:
    """Create a temporary bucket to store optimization output."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET)

    yield

    bucket.delete(force=True)


def test_call_async_api(capsys: pytest.LogCaptureFixture) -> None:
    _, project_id = google.auth.default()
    async_api.call_async_api(project_id, INPUT_URI, BATCH_OUTPUT_URI_PREFIX)
    out, _ = capsys.readouterr()

    assert "operations" in out
