# Copyright 2021 Google LLC
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

from google.cloud import storage
import pytest


import translate_v3beta1_batch_translate_document


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="function")
def bucket():
    # Create a temporary bucket to store annotation output.
    bucket_name = f"test-{uuid.uuid4()}"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket = storage_client.create_bucket(bucket, location="us-central1")

    yield bucket

    bucket.delete(force=True)


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_batch_translate_document(capsys, bucket):
    translate_v3beta1_batch_translate_document.batch_translate_document(
        input_uri="gs://cloud-samples-data/translation/async_invoices/*",
        output_uri=f"gs://{bucket.name}/translation/BATCH_TRANSLATE_DOCUMENT_OUTPUT/",
        project_id=PROJECT_ID,
        timeout=1000,
    )

    out, _ = capsys.readouterr()
    assert "Total Pages" in out
