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

from google.cloud import aiplatform

import gemma3_deploy
import models_deploy_options_list
import models_deployable_list


def test_list_deployable_models() -> None:
    models = models_deployable_list.list_deployable_models()
    assert len(models) > 0
    assert "gemma" in models[0]


def test_list_deploy_options() -> None:
    deploy_options = models_deploy_options_list.list_deploy_options(
        model="google/gemma3@gemma-3-1b-it"
    )
    assert len(deploy_options) > 0


@patch("vertexai.preview.model_garden.OpenModel")
def test_gemma3_deploy(mock_open_model: MagicMock) -> None:
    # Mock the deploy response.
    mock_endpoint = aiplatform.Endpoint(endpoint_name="test-endpoint-name")
    mock_open_model.return_value.deploy.return_value = mock_endpoint
    endpoint = gemma3_deploy.deploy()
    assert endpoint
    mock_open_model.assert_called_once_with("google/gemma3@gemma-3-12b-it")
    mock_open_model.return_value.deploy.assert_called_once_with(
        machine_type="g2-standard-48",
        accelerator_type="NVIDIA_L4",
        accelerator_count=4,
        accept_eula=True,
    )
