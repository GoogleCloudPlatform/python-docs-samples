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

#
# Using Google Cloud Vertex AI to test the code samples.
#

from datetime import datetime as dt

import os

from google.cloud import bigquery, storage
from google.genai.types import JobState

import pytest

import anthropic_batchpredict_with_bq
import anthropic_batchpredict_with_gcs


os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-east5"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"
BQ_OUTPUT_DATASET = f"{os.environ['GOOGLE_CLOUD_PROJECT']}.anthropic_bq_sample"
GCS_OUTPUT_BUCKET = "python-docs-samples-tests"


@pytest.fixture(scope="session")
def bq_output_uri() -> str:
    table_name = f"text_output_{dt.now().strftime('%Y_%m_%d_T%H_%M_%S')}"
    table_uri = f"{BQ_OUTPUT_DATASET}.{table_name}"

    yield f"bq://{table_uri}"

    bq_client = bigquery.Client()
    bq_client.delete_table(table_uri, not_found_ok=True)


@pytest.fixture(scope="session")
def gcs_output_uri() -> str:
    prefix = f"text_output/{dt.now()}"

    yield f"gs://{GCS_OUTPUT_BUCKET}/{prefix}"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCS_OUTPUT_BUCKET)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        blob.delete()


def test_batch_prediction_with_bq(bq_output_uri: str) -> None:
    response = anthropic_batchpredict_with_bq.generate_content(output_uri=bq_output_uri)
    assert response == JobState.JOB_STATE_SUCCEEDED


def test_batch_prediction_with_gcs(gcs_output_uri: str) -> None:
    response = anthropic_batchpredict_with_gcs.generate_content(output_uri=gcs_output_uri)
    assert response == JobState.JOB_STATE_SUCCEEDED
