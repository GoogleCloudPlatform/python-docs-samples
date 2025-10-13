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
from unittest.mock import MagicMock, patch

from google.genai import types
from google.genai.types import JobState

import batchpredict_embeddings_with_gcs
import batchpredict_with_bq
import batchpredict_with_gcs
import get_batch_job


@patch("google.genai.Client")
@patch("time.sleep", return_value=None)
def test_batch_prediction_embeddings_with_gcs(
    mock_sleep: MagicMock, mock_genai_client: MagicMock
) -> None:
    # Mock the API response
    mock_batch_job_running = types.BatchJob(
        name="test-batch-job", state="JOB_STATE_RUNNING"
    )
    mock_batch_job_succeeded = types.BatchJob(
        name="test-batch-job", state="JOB_STATE_SUCCEEDED"
    )

    mock_genai_client.return_value.batches.create.return_value = (
        mock_batch_job_running
    )
    mock_genai_client.return_value.batches.get.return_value = (
        mock_batch_job_succeeded
    )

    response = batchpredict_embeddings_with_gcs.generate_content(
        output_uri="gs://test-bucket/test-prefix"
    )

    mock_genai_client.assert_called_once_with(
        http_options=types.HttpOptions(api_version="v1")
    )
    mock_genai_client.return_value.batches.create.assert_called_once()
    mock_genai_client.return_value.batches.get.assert_called_once()
    assert response == JobState.JOB_STATE_SUCCEEDED


@patch("google.genai.Client")
@patch("time.sleep", return_value=None)
def test_batch_prediction_with_bq(
    mock_sleep: MagicMock, mock_genai_client: MagicMock
) -> None:
    # Mock the API response
    mock_batch_job_running = types.BatchJob(
        name="test-batch-job", state="JOB_STATE_RUNNING"
    )
    mock_batch_job_succeeded = types.BatchJob(
        name="test-batch-job", state="JOB_STATE_SUCCEEDED"
    )

    mock_genai_client.return_value.batches.create.return_value = (
        mock_batch_job_running
    )
    mock_genai_client.return_value.batches.get.return_value = (
        mock_batch_job_succeeded
    )

    response = batchpredict_with_bq.generate_content(
        output_uri="bq://test-project.test_dataset.test_table"
    )

    mock_genai_client.assert_called_once_with(
        http_options=types.HttpOptions(api_version="v1")
    )
    mock_genai_client.return_value.batches.create.assert_called_once()
    mock_genai_client.return_value.batches.get.assert_called_once()
    assert response == JobState.JOB_STATE_SUCCEEDED


@patch("google.genai.Client")
@patch("time.sleep", return_value=None)
def test_batch_prediction_with_gcs(
    mock_sleep: MagicMock, mock_genai_client: MagicMock
) -> None:
    # Mock the API response
    mock_batch_job_running = types.BatchJob(
        name="test-batch-job", state="JOB_STATE_RUNNING"
    )
    mock_batch_job_succeeded = types.BatchJob(
        name="test-batch-job", state="JOB_STATE_SUCCEEDED"
    )

    mock_genai_client.return_value.batches.create.return_value = (
        mock_batch_job_running
    )
    mock_genai_client.return_value.batches.get.return_value = (
        mock_batch_job_succeeded
    )

    response = batchpredict_with_gcs.generate_content(
        output_uri="gs://test-bucket/test-prefix"
    )

    mock_genai_client.assert_called_once_with(
        http_options=types.HttpOptions(api_version="v1")
    )
    mock_genai_client.return_value.batches.create.assert_called_once()
    mock_genai_client.return_value.batches.get.assert_called_once()
    assert response == JobState.JOB_STATE_SUCCEEDED


@patch("google.genai.Client")
def test_get_batch_job(mock_genai_client: MagicMock) -> None:
    # Mock the API response
    mock_batch_job = types.BatchJob(name="test-batch-job", state="JOB_STATE_PENDING")

    mock_genai_client.return_value.batches.get.return_value = mock_batch_job

    response = get_batch_job.get_batch_job("test-batch-job")

    mock_genai_client.assert_called_once_with(
        http_options=types.HttpOptions(api_version="v1")
    )
    mock_genai_client.return_value.batches.get.assert_called_once()
    assert response == mock_batch_job
