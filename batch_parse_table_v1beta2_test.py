# Copyright 2020 Google LLC
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
# See the License for the specific ladnguage governing permissions and
# limitations under the License.

import os
import uuid

from google.cloud import storage
import pytest
from samples.snippets import batch_parse_table_v1beta2

BUCKET = "document-ai-{}".format(uuid.uuid4())
OUTPUT_PREFIX = "TEST_OUTPUT_{}".format(uuid.uuid4())
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
INPUT_URI = "gs://cloud-samples-data/documentai/invoice.pdf"
BATCH_OUTPUT_URI = "gs://{}/{}/".format(BUCKET, OUTPUT_PREFIX)


@pytest.fixture(autouse=True)
def setup_teardown():
    """Create a temporary bucket to store annotation output."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET)

    yield

    bucket.delete(force=True)


def test_batch_parse_table(capsys):
    batch_parse_table_v1beta2.batch_parse_table(
        PROJECT_ID, INPUT_URI, BATCH_OUTPUT_URI, 120
    )
    out, _ = capsys.readouterr()
    assert "Output files:" in out
