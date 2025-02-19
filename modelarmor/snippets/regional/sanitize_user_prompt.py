# python-docs-samples/modelarmor/sanitize_user_prompt.py

# Copyright 2021 Google LLC
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

import argparse

# [START sanitize_user_prompt]
def sanitize_user_prompt(project_id: str, location_id: str, template_id: str, payload: dict = None):
    """
    Sanitizes a user prompt using the Model Armor API.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.
        payload (str, optional): Request payload for user prompt sanitization.
    Returns:
        Dict: The sanitized prompt response.
    """
    from google.cloud import modelarmor_v1
    from google.cloud.modelarmor_v1.types import SanitizeUserPromptRequest
    from google.api_core.client_options import ClientOptions

    # Initialize the Model Armor client
    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )

    # Sanitize the user prompt
    request = SanitizeUserPromptRequest(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        user_prompt_data=payload["user_prompt_data"]
    )
    
    # Sanitize the user prompt
    response = client.sanitize_user_prompt(request=request)
    
    print(f"Sanitized prompt: {response}")
    # [END sanitize_user_prompt] 
    return response

if __name__ == "__main__":
    # Sample usage with text data
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("location_id", help="Google Cloud location")
    parser.add_argument("template_id", help="The template ID used for sanitization")
    parser.add_argument("model_response", help="The model response data to sanitize")

    args = parser.parse_args()

    sanitize_user_prompt(args.project_id, args.location_id, args.template_id, args.payload)
