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
Sample code for scanning a PDF file content using model armor.
"""

from google.cloud import modelarmor_v1


def screen_pdf_file(
    project_id: str,
    location_id: str,
    template_id: str,
    pdf_content_filename: str,
) -> modelarmor_v1.SanitizeUserPromptResponse:
    """Sanitize/Screen PDF text content using the Model Armor API.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.
        template_id (str): The template ID used for sanitization.
        pdf_content_filename (str): Path to a PDF file.

    Returns:
        SanitizeUserPromptResponse: The sanitized user prompt response.
    """
    # [START modelarmor_screen_pdf_file]

    import base64
    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "YOUR_PROJECT_ID"
    # location_id = "us-central1"
    # template_id = "template_id"
    # pdf_content_filename = "path/to/file.pdf"

    # Encode the PDF file into base64
    with open(pdf_content_filename, "rb") as f:
        pdf_content_base64 = base64.b64encode(f.read())

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com"
        ),
    )

    # Initialize request argument(s).
    user_prompt_data = modelarmor_v1.DataItem(
        byte_item=modelarmor_v1.ByteDataItem(
            byte_data_type=modelarmor_v1.ByteDataItem.ByteItemType.PDF,
            byte_data=pdf_content_base64,
        )
    )

    request = modelarmor_v1.SanitizeUserPromptRequest(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        user_prompt_data=user_prompt_data,
    )

    # Sanitize the user prompt.
    response = client.sanitize_user_prompt(request=request)

    # Sanitization Result.
    print(response)

    # [END modelarmor_screen_pdf_file]

    return response
