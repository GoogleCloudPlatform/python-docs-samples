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

from vertexai.generative_models import (
    GenerationResponse,
    GenerativeModel,
)

import api_key_example


@patch.object(GenerativeModel, "generate_content")
def test_api_key_example(mock_generate_content: MagicMock) -> None:
    # Mock the API response
    mock_generate_content.return_value = GenerationResponse.from_dict(
        {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "This is a mocked bubble sort explanation."}]
                    }
                }
            ]
        }
    )

    # Call the function
    response = api_key_example.generate_content()

    # Assert that the function returns the expected value
    assert response == "This is a mocked bubble sort explanation."
