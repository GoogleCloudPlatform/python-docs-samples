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
Sample code for creating a new model armor template with labels.
"""

from google.cloud import modelarmor_v1


def create_model_armor_template_with_labels(
    project_id: str,
    location_id: str,
    template_id: str,
    labels: dict,
) -> modelarmor_v1.Template:
    """
    Creates a new model armor template with labels.

    Args:
        project_id (str): Google Cloud project ID where the template will be created.
        location_id (str): Google Cloud location where the template will be created.
        template_id (str): ID for the template to create.
        labels (dict): Configuration for the labels of the template.
            eg. {"key1": "value1", "key2": "value2"}

    Returns:
        Template: The created Template.
    """
    # [START modelarmor_create_template_with_labels]

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

    parent = f"projects/{project_id}/locations/{location_id}"

    # Build the Model Armor template with your preferred filters.
    # For more details on filters, please refer to the following doc:
    # https://cloud.google.com/security-command-center/docs/key-concepts-model-armor#ma-filters
    template = modelarmor_v1.Template(
        filter_config=modelarmor_v1.FilterConfig(
            rai_settings=modelarmor_v1.RaiFilterSettings(
                rai_filters=[
                    modelarmor_v1.RaiFilterSettings.RaiFilter(
                        filter_type=modelarmor_v1.RaiFilterType.HATE_SPEECH,
                        confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                    ),
                    modelarmor_v1.RaiFilterSettings.RaiFilter(
                        filter_type=modelarmor_v1.RaiFilterType.SEXUALLY_EXPLICIT,
                        confidence_level=modelarmor_v1.DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
                    ),
                ]
            )
        ),
        labels=labels,
    )

    # Prepare the request for creating the template.
    create_template = modelarmor_v1.CreateTemplateRequest(
        parent=parent, template_id=template_id, template=template
    )

    # Create the template.
    response = client.create_template(request=create_template)

    # Print the new template name.
    print(f"Created template: {response.name}")

    # [END modelarmor_create_template_with_labels]

    return response
