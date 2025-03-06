# Copyright 2024 Google LLC
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
import os
from typing import Callable

import backoff
from google.api_core.exceptions import ResourceExhausted
from google.cloud import storage
from google.cloud.aiplatform import BatchPredictionJob
from google.cloud.aiplatform_v1 import JobState
import pytest

import claude_3_batch_prediciton_bq
import claude_3_batch_prediction_gcs
import claude_3_streaming_example
import claude_3_tool_example
import claude_3_unary_example

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

INPUT_BUCKET = "kellysun-test-project-europe-west1"
OUTPUT_BUCKET = "python-docs-samples-tests"
OUTPUT_PATH = "batch/batch_text_predict_output"
GCS_OUTPUT_PATH = "gs://python-docs-samples-tests/"
OUTPUT_TABLE = f"bq://{PROJECT_ID}.gen_ai_batch_prediction.predictions"


def _clean_resources() -> None:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(OUTPUT_BUCKET)
    blobs = bucket.list_blobs(prefix=OUTPUT_PATH)
    for blob in blobs:
        blob.delete()


@pytest.fixture(scope="session")
def output_folder() -> str:
    yield f"gs://{OUTPUT_BUCKET}/{OUTPUT_PATH}"
    _clean_resources()


def _main_test(test_func: Callable) -> BatchPredictionJob:
    job = None
    try:
        job = test_func()
        assert job.state == JobState.JOB_STATE_SUCCEEDED
        return job
    finally:
        if job is not None:
            job.delete()


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_generate_text_streaming() -> None:
    responses = claude_3_streaming_example.generate_text_streaming()
    assert "bread" in responses


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_tool_use() -> None:
    response = claude_3_tool_example.tool_use()
    json_response = response.model_dump_json(indent=2)
    assert "restaurant" in json_response
    assert "tool_use" in json_response
    assert "text_search_places_api" in json_response


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_generate_text() -> None:
    responses = claude_3_unary_example.generate_text()
    assert "bread" in responses.model_dump_json(indent=2)


def test_batch_gemini_predict_gcs(output_folder: pytest.fixture()) -> None:
    output_uri = "gs://python-docs-samples-tests"
    job = _main_test(
        test_func=lambda: claude_3_batch_prediction_gcs.batch_predict_gemini_createjob(
            output_uri
        )
    )
    assert GCS_OUTPUT_PATH in job.output_location


def test_batch_gemini_predict_bigquery(output_folder: pytest.fixture()) -> None:
    output_uri = f"bq://{PROJECT_ID}.gen_ai_batch_prediction.predictions"
    job = _main_test(
        test_func=lambda: claude_3_batch_prediciton_bq.batch_predict_gemini_createjob(
            output_uri
            )
    )
    assert OUTPUT_TABLE in job.output_location
