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
from typing import MutableSequence, Optional
from unittest import mock
from unittest.mock import MagicMock

from google.cloud.aiplatform_v1.types import prediction_service
import google.protobuf.struct_pb2 as struct_pb2
from google.protobuf.struct_pb2 import Value

from gemma2_predict_gpu import gemma2_predict_gpu
from gemma2_predict_tpu import gemma2_predict_tpu

# Global variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
GPU_ENDPOINT_REGION = "us-east1"
GPU_ENDPOINT_ID = "123456789"  # Mock ID used to check if GPU was called

TPU_ENDPOINT_REGION = "us-west1"
TPU_ENDPOINT_ID = "987654321"  # Mock ID used to check if TPU was called

# MOCKED RESPONSE
MODEL_RESPONSES = """
The sky appears blue due to a phenomenon called **Rayleigh scattering**.

**Here's how it works:**

1. **Sunlight:** Sunlight is composed of all the colors of the rainbow.

2. **Earth's Atmosphere:** When sunlight enters the Earth's atmosphere, it collides with tiny particles like nitrogen and oxygen molecules.

3. **Scattering:** These particles scatter the sunlight in all directions. However, blue light (which has a shorter wavelength) is scattered more effectively than other colors.

4. **Our Perception:** As a result, we see a blue sky because the scattered blue light reaches our eyes from all directions.

**Why not other colors?**

* **Violet light** has an even shorter wavelength than blue and is scattered even more. However, our eyes are less sensitive to violet light, so we perceive the sky as blue.
* **Longer wavelengths** like red, orange, and yellow are scattered less and travel more directly through the atmosphere. This is why we see these colors during sunrise and sunset, when sunlight has to travel through more of the atmosphere.
"""


# Mocked function - we check if proper format was used depending on selected architecture
def mock_predict(
    endpoint: Optional[str] = None,
    instances: Optional[MutableSequence[struct_pb2.Value]] = None,
) -> prediction_service.PredictResponse:
    gpu_endpoint = f"projects/{PROJECT_ID}/locations/{GPU_ENDPOINT_REGION}/endpoints/{GPU_ENDPOINT_ID}"
    tpu_endpoint = f"projects/{PROJECT_ID}/locations/{TPU_ENDPOINT_REGION}/endpoints/{TPU_ENDPOINT_ID}"
    instance_fields = instances[0].struct_value.fields

    if endpoint == gpu_endpoint:
        assert "string_value" in instance_fields["inputs"]
        assert "struct_value" in instance_fields["parameters"]
        parameters = instance_fields["parameters"].struct_value.fields
        assert "number_value" in parameters["max_tokens"]
        assert "number_value" in parameters["temperature"]
        assert "number_value" in parameters["top_p"]
        assert "number_value" in parameters["top_k"]
    elif endpoint == tpu_endpoint:
        assert "string_value" in instance_fields["prompt"]
        assert "number_value" in instance_fields["max_tokens"]
        assert "number_value" in instance_fields["temperature"]
        assert "number_value" in instance_fields["top_p"]
        assert "number_value" in instance_fields["top_k"]
    else:
        assert False

    response = prediction_service.PredictResponse()
    response.predictions.append(Value(string_value=MODEL_RESPONSES))
    return response


@mock.patch("google.cloud.aiplatform.gapic.PredictionServiceClient")
def test_gemma2_predict_gpu(mock_client: MagicMock) -> None:
    mock_client_instance = mock_client.return_value
    mock_client_instance.predict = mock_predict

    response = gemma2_predict_gpu(GPU_ENDPOINT_REGION, GPU_ENDPOINT_ID)
    assert "Rayleigh scattering" in response


@mock.patch("google.cloud.aiplatform.gapic.PredictionServiceClient")
def test_gemma2_predict_tpu(mock_client: MagicMock) -> None:
    mock_client_instance = mock_client.return_value
    mock_client_instance.predict = mock_predict

    response = gemma2_predict_tpu(TPU_ENDPOINT_REGION, TPU_ENDPOINT_ID)
    assert "Rayleigh scattering" in response
