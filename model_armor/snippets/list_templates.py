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
Sample code for getting list of model armor templates.
"""

from google.cloud.modelarmor_v1.services.model_armor import pagers


def list_model_armor_templates(
    project_id: str,
    location: str,
) -> pagers.ListTemplatesPager:
    """List model armor templates.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.

    Returns:
        ListTemplatesPager: List of model armor templates.
    """
    # [START modelarmor_list_templates]
    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location}.rep.googleapis.com"
        ),
    )

    # Initialize request argument(s).
    request = modelarmor_v1.ListTemplatesRequest(
        parent=f"projects/{project_id}/locations/{location}"
    )

    # Get list of templates.
    response = client.list_templates(request=request)
    for template in response:
        print(template.name)

    # [END modelarmor_list_templates]

    return response
