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
Sample code for getting a model armor template.
"""

from google.cloud import modelarmor_v1


def get_model_armor_template(
    project_id: str,
    location: str,
    template_id: str,
) -> modelarmor_v1.Template:
    """Get model armor template.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.
        template_id (str): ID for the template to create.

    Returns:
        Template: Fetched model armor template
    """
    # [START modelarmor_get_template]

    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"
    # template_id = "template_id"

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location}.rep.googleapis.com"
        ),
    )

    # Initialize request arguments.
    request = modelarmor_v1.GetTemplateRequest(
        name=f"projects/{project_id}/locations/{location}/templates/{template_id}",
    )

    # Get the template.
    response = client.get_template(request=request)
    print(response.name)

    # [END modelarmor_get_template]

    return response
