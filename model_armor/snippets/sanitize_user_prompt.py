# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Sample code for sanitizing user prompt with model armor.
"""

from google.cloud import modelarmor_v1


def sanitize_user_prompt(
    project_id: str,
    location_id: str,
    template_id: str,
    user_prompt: str,
) -> modelarmor_v1.SanitizeUserPromptResponse:
    """
    Sanitizes a user prompt using the Model Armor API.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.
        template_id (str): The template ID used for sanitization.
        user_prompt (str): Prompt entered by the user.

    Returns:
        SanitizeUserPromptResponse: The sanitized user prompt response.
    """
    # [START modelarmor_sanitize_user_prompt]

    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"
    # template_id = "template_id"
    # user_prompt = "Prompt entered by the user"

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com"
        ),
    )

    # Initialize request argument(s).
    user_prompt_data = modelarmor_v1.DataItem(text=user_prompt)

    # Prepare request for sanitizing the defined prompt.
    request = modelarmor_v1.SanitizeUserPromptRequest(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        user_prompt_data=user_prompt_data,
    )

    # Sanitize the user prompt.
    response = client.sanitize_user_prompt(request=request)

    # Sanitization Result.
    print(response)

    # [END modelarmor_sanitize_user_prompt]

    return response
