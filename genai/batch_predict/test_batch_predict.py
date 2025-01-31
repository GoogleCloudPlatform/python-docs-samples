# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime as dt, UTC
import os

from google.cloud import storage
from google.genai.types import JobState
import pytest

import batch_prediction_with_gcs


os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"
GCS_OUTPUT_BUCKET = "python-docs-samples-tests"
GCS_OUTPUT_BUCKET = "gemini-batch-prediction-results"


@pytest.fixture(scope="session")
def gcs_output_uri():
    prefix = f"text_output/{dt.now(UTC)}"

    yield f"gs://{GCS_OUTPUT_BUCKET}/{prefix}"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCS_OUTPUT_BUCKET)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        blob.delete()


def test_batch_prediction_with_gcs(gcs_output_uri) -> None:
    job = batch_prediction_with_gcs.create_job(output_uri=gcs_output_uri)
    assert job
    assert job.state == "JOB_STATE_SUCCEEDED"
    assert job.dest.gcs_uri == gcs_output_uri
    assert job.state == JobState.JOB_STATE_SUCCEEDED
