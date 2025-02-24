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
Sample code for updating the labels of the given model armor template.
"""

from typing import Dict

from google.cloud import modelarmor_v1


def update_model_armor_template_labels(
    project_id: str,
    location_id: str,
    template_id: str,
    labels: Dict,
) -> modelarmor_v1.Template:
    """
    Updates the labels of the given model armor template.

    Args:
        project_id (str): Google Cloud project ID where the template exists.
        location_id (str): Google Cloud location where the template exists.
        template_id (str): ID of the template to update.
        labels (Dict): Labels in key, value pair
            eg. {"key1": "value1", "key2": "value2"}

    Returns:
        Template: The updated Template.
    """
    # [START modelarmor_update_template_with_labels]

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

    # Build the Model Armor template with your preferred filters.
    # For more details on filters, please refer to the following doc:
    # https://cloud.google.com/security-command-center/docs/key-concepts-model-armor#ma-filters
    template = modelarmor_v1.Template(
        name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        labels=labels,
    )

    # Prepare the request to update the template.
    updated_template = modelarmor_v1.UpdateTemplateRequest(
        template=template, update_mask={"paths": ["labels"]}
    )

    # Update the template.
    response = client.update_template(request=updated_template)

    print(f"Updated Model Armor Template: {response.name}")

    # [END modelarmor_update_template_with_labels]

    return response
