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
Sample code for sanitizing a model response using the model armor.
"""

from google.cloud import modelarmor_v1


def sanitize_model_response(
    project_id: str,
    location_id: str,
    template_id: str,
    model_response: str,
) -> modelarmor_v1.SanitizeModelResponseResponse:
    """
    Sanitizes a model response using the Model Armor API.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.
        template_id (str): The template ID used for sanitization.
        model_response (str): The model response data to sanitize.

    Returns:
        SanitizeModelResponseResponse: The sanitized model response.
    """
    # [START modelarmor_sanitize_model_response]

    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "YOUR_PROJECT_ID"
    # location_id = "us-central1"
    # template_id = "template_id"
    # model_response = "The model response data to sanitize"

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com"
        )
    )

    # Initialize request argument(s)
    model_response_data = modelarmor_v1.DataItem(text=model_response)

    # Prepare request for sanitizing model response.
    request = modelarmor_v1.SanitizeModelResponseRequest(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        model_response_data=model_response_data,
    )

    # Sanitize the model response.
    response = client.sanitize_model_response(request=request)

    # Sanitization Result.
    print(response)

    # [END modelarmor_sanitize_model_response]

    return response
