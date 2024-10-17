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

import pytest
from unittest import mock
from google.cloud import aiplatform
from google.cloud.aiplatform import models

# Interfaces defined here:
# https://github.com/googleapis/python-aiplatform/blob/main/google/cloud/aiplatform/models.py

from gemma2_predict_gpu import endpoint_predict_sample


@pytest.fixture
def mock_init():
    return mock.Mock(spec=aiplatform.init)


@pytest.fixture
def mock_prediction():
    return mock.Mock(spec=models.Prediction)


@pytest.fixture
def mock_endpoint():
    return mock.Mock(spec=aiplatform.Endpoint)


@mock.patch("google.cloud.aiplatform.Endpoint")
@mock.patch("google.cloud.aiplatform.models.Prediction")
@mock.patch("google.cloud.aiplatform.init")
def test_gemma2_predict_gpu(mock_init, mock_prediction, mock_endpoint):
    mock_endpoint.return_value.predict.return_value = mock_prediction

    project_id = "fake-proj"
    location = "fake-place"
    instance = "Why is the sky blue?"
    endpoint = "fake_endpoint_id"

    prediction = endpoint_predict_sample(
        project=project_id, location=location, instances=[instance], endpoint=endpoint
    )

    assert prediction
