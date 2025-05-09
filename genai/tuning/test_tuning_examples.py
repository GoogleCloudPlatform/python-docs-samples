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

import tuning_job_create
import tuning_job_get
import tuning_job_list
import tuning_textgen_with_txt


@patch("google.genai.Client")
def test_tuning_job_create(mock_genai_client: MagicMock) -> None:
    # Mock the API response
    mock_tuning_job = types.TuningJob(
        name="test-tuning-job",
        experiment="test-experiment",
        tuned_model=types.TunedModel(
            model="test-model",
            endpoint="test-endpoint"
        )
    )
    mock_genai_client.return_value.tunings.tune.return_value = mock_tuning_job

    response = tuning_job_create.create_tuning_job()

    mock_genai_client.assert_called_once_with(http_options=types.HttpOptions(api_version="v1"))
    mock_genai_client.return_value.tunings.tune.assert_called_once()
    assert response == "test-tuning-job"


@patch("google.genai.Client")
def test_tuning_job_get(mock_genai_client: MagicMock) -> None:
    # Mock the API response
    mock_tuning_job = types.TuningJob(
        name="test-tuning-job",
        experiment="test-experiment",
        tuned_model=types.TunedModel(
            model="test-model",
            endpoint="test-endpoint"
        )
    )
    mock_genai_client.return_value.tunings.get.return_value = mock_tuning_job

    response = tuning_job_get.get_tuning_job("test-tuning-job")

    mock_genai_client.assert_called_once_with(http_options=types.HttpOptions(api_version="v1"))
    mock_genai_client.return_value.tunings.get.assert_called_once()
    assert response == "test-tuning-job"


@patch("google.genai.Client")
def test_tuning_job_list(mock_genai_client: MagicMock) -> None:
    # Mock the API response
    mock_tuning_job = types.TuningJob(
        name="test-tuning-job",
        experiment="test-experiment",
        tuned_model=types.TunedModel(
            model="test-model",
            endpoint="test-endpoint"
        )
    )
    mock_genai_client.return_value.tunings.list.return_value = [mock_tuning_job]

    tuning_job_list.list_tuning_jobs()

    mock_genai_client.assert_called_once_with(http_options=types.HttpOptions(api_version="v1"))
    mock_genai_client.return_value.tunings.list.assert_called_once()


@patch("google.genai.Client")
def test_tuning_textgen_with_txt(mock_genai_client: MagicMock) -> None:
    # Mock the API response
    mock_tuning_job = types.TuningJob(
        name="test-tuning-job",
        experiment="test-experiment",
        tuned_model=types.TunedModel(
            model="test-model",
            endpoint="test-endpoint"
        )
    )
    mock_response = types.GenerateContentResponse._from_response(  # pylint: disable=protected-access
        response={
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "This is a mocked answer."}]
                    }
                }
            ]
        },
        kwargs={},
    )

    mock_genai_client.return_value.tunings.get.return_value = mock_tuning_job
    mock_genai_client.return_value.models.generate_content.return_value = mock_response

    tuning_textgen_with_txt.test_tuned_endpoint("test-tuning-job")

    mock_genai_client.assert_called_once_with(http_options=types.HttpOptions(api_version="v1"))
    mock_genai_client.return_value.tunings.get.assert_called_once()
    mock_genai_client.return_value.models.generate_content.assert_called_once()
