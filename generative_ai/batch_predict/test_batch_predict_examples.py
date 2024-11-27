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


from google.cloud import storage
from google.cloud.aiplatform import BatchPredictionJob
from google.cloud.aiplatform_v1 import JobState


import pytest


import batch_code_predict
import batch_text_predict
import gemini_batch_predict_bigquery
import gemini_batch_predict_gcs

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


INPUT_BUCKET = "cloud-samples-data"
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


def test_batch_text_predict(output_folder: pytest.fixture()) -> None:
    input_uri = f"gs://{INPUT_BUCKET}/batch/prompt_for_batch_text_predict.jsonl"
    job = _main_test(
        test_func=lambda: batch_text_predict.batch_text_prediction(
            input_uri, output_folder
        )
    )
    assert OUTPUT_PATH in job.output_info.gcs_output_directory


def test_batch_code_predict(output_folder: pytest.fixture()) -> None:
    input_uri = f"gs://{INPUT_BUCKET}/batch/prompt_for_batch_code_predict.jsonl"
    job = _main_test(
        test_func=lambda: batch_code_predict.batch_code_prediction(
            input_uri, output_folder
        )
    )
    assert OUTPUT_PATH in job.output_info.gcs_output_directory


def test_batch_gemini_predict_gcs(output_folder: pytest.fixture()) -> None:
    output_uri = "gs://python-docs-samples-tests"
    job = _main_test(
        test_func=lambda: gemini_batch_predict_gcs.batch_predict_gemini_createjob(
            output_uri
        )
    )
    assert GCS_OUTPUT_PATH in job.output_location


def test_batch_gemini_predict_bigquery(output_folder: pytest.fixture()) -> None:
    output_uri = f"bq://{PROJECT_ID}.gen_ai_batch_prediction.predictions"
    job = _main_test(
        test_func=lambda: gemini_batch_predict_bigquery.batch_predict_gemini_createjob(
            output_uri
            )
    )
    assert OUTPUT_TABLE in job.output_location
