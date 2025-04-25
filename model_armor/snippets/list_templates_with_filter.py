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
Sample code for listing model armor templates with filters.
"""

from typing import List


def list_model_armor_templates_with_filter(
    project_id: str,
    location_id: str,
    template_id: str,
) -> List[str]:
    """
    Lists all model armor templates in the specified project and location.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.
        template_id (str): Model Armour Template ID(s) to filter from list.

    Returns:
        List[str]: A list of template names.
    """
    # [START modelarmor_list_templates_with_filter]

    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "YOUR_PROJECT_ID"
    # location_id = "us-central1"
    # template_id = "template_id"

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com"
        ),
    )

    # Preparing the parent path
    parent = f"projects/{project_id}/locations/{location_id}"

    # Get the list of templates
    templates = client.list_templates(
        request=modelarmor_v1.ListTemplatesRequest(
            parent=parent, filter=f'name="{parent}/templates/{template_id}"'
        )
    )

    # Print templates name only
    templates_name = [template.name for template in templates]
    print(
        f"Templates Found: {', '.join(template_name for template_name in templates_name)}"
    )
    # [END modelarmor_list_templates_with_filter]

    return templates
