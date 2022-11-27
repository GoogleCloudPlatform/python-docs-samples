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
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from uuid import uuid4

from google.cloud import storage
from google.cloud.exceptions import NotFound
import pytest
from samples.snippets import batch_process_documents_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
processor_id = "90484cfdedb024f6"
gcs_input_uri = "gs://cloud-samples-data/documentai/invoice.pdf"
input_mime_type = "application/pdf"
gcs_output_uri_prefix = f"{uuid4()}/"
field_mask = "text,pages.pageNumber"
BUCKET_NAME = f"document-ai-python-{uuid4()}"


@pytest.fixture(scope="module")
def test_bucket():
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)
    yield bucket.name

    try:
        blobs = list(bucket.list_blobs())
        for blob in blobs:
            blob.delete()
        bucket.delete()
    except NotFound:
        print("Bucket already deleted.")


def test_batch_process_documents(capsys, test_bucket):
    batch_process_documents_sample.batch_process_documents(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        gcs_input_uri=gcs_input_uri,
        input_mime_type=input_mime_type,
        gcs_output_bucket=f"gs://{test_bucket}",
        gcs_output_uri_prefix=gcs_output_uri_prefix,
        field_mask=field_mask,
    )
    out, _ = capsys.readouterr()

    assert "operation" in out
    assert "Fetching" in out
    assert "text:" in out
