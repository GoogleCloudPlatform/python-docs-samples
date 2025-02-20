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

from google.cloud.modelarmor_v1 import SanitizeUserPromptResponse


def sanitize_user_prompt(
    project_id: str, location: str, template_id: str
) -> SanitizeUserPromptResponse:
    # [START modelarmor_sanitize_user_prompt]

    from google.api_core.client_options import ClientOptions
    from google.cloud.modelarmor_v1 import (
        ModelArmorClient,
        DataItem,
        SanitizeUserPromptRequest
    )

    client = ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location}.rep.googleapis.com"),
    )

    # TODO(Developer): Uncomment these variables and initialize
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"
    # template_id = "template_id"

    # Define the prompt
    user_prompt = "Can you describe this link? https://testsafebrowsing.appspot.com/s/malware.html"

    # Initialize request argument(s)
    user_prompt_data = DataItem(
        text=user_prompt
    )

    request = SanitizeUserPromptRequest(
        name=f"projects/{project_id}/locations/{location}/templates/{template_id}",
        user_prompt_data=user_prompt_data,
    )

    # Make the request
    response = client.sanitize_user_prompt(request=request)
    # Match state is TRUE when the prompt is caught by one of the safety policies in the template.
    print(response.sanitization_result.filter_match_state)

# [END modelarmor_sanitize_user_prompt]

    # Handle the response
    return response
