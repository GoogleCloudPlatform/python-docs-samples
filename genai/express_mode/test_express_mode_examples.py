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

import api_key_example


@patch("google.genai.Client")
def test_api_key_example(mock_genai_client: MagicMock) -> None:
    # Mock the API response
    mock_response = types.GenerateContentResponse._from_response(  # pylint: disable=protected-access
        response={
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "This is a mocked bubble sort explanation."}]
                    }
                }
            ]
        },
        kwargs={},
    )
    mock_genai_client.return_value.models.generate_content.return_value = mock_response

    response = api_key_example.generate_content()

    mock_genai_client.assert_called_once_with(vertexai=True, api_key="YOUR_API_KEY")
    mock_genai_client.return_value.models.generate_content.assert_called_once_with(
        model="gemini-2.5-flash-preview-05-20",
        contents="Explain bubble sort to me.",
    )
    assert response == "This is a mocked bubble sort explanation."
