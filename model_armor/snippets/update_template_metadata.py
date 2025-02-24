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
Sample code for updating the model armor template metadata.
"""

from google.cloud import modelarmor_v1


def update_model_armor_template_metadata(
    project_id: str,
    location_id: str,
    template_id: str,
) -> modelarmor_v1.Template:
    """
    Updates an existing model armor template.

    Args:
        project_id (str): Google Cloud project ID where the template exists.
        location_id (str): Google Cloud location where the template exists.
        template_id (str): ID of the template to update.
        updated_filter_config_data (Dict): Updated configuration for the filter
            settings of the template.

    Returns:
        Template: The updated Template.
    """
    # [START modelarmor_update_template_metadata]

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

    # Build the full resource path for the template.
    template_name = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    # Build the Model Armor template with your preferred filters.
    # For more details on filters, please refer to the following doc:
    # https://cloud.google.com/security-command-center/docs/key-concepts-model-armor#ma-filters
    template = modelarmor_v1.Template(
        name=template_name,
        filter_config=modelarmor_v1.FilterConfig(
            rai_settings=modelarmor_v1.RaiFilterSettings(
                rai_filters=[
                    modelarmor_v1.RaiFilterSettings.RaiFilter(
                        filter_type=modelarmor_v1.RaiFilterType.DANGEROUS,
                        confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                    ),
                    modelarmor_v1.RaiFilterSettings.RaiFilter(
                        filter_type=modelarmor_v1.RaiFilterType.HARASSMENT,
                        confidence_level=modelarmor_v1.DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
                    ),
                    modelarmor_v1.RaiFilterSettings.RaiFilter(
                        filter_type=modelarmor_v1.RaiFilterType.HATE_SPEECH,
                        confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                    ),
                    modelarmor_v1.RaiFilterSettings.RaiFilter(
                        filter_type=modelarmor_v1.RaiFilterType.SEXUALLY_EXPLICIT,
                        confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                    ),
                ]
            ),
            sdp_settings=modelarmor_v1.SdpFilterSettings(
                basic_config=modelarmor_v1.SdpBasicConfig(
                    filter_enforcement=modelarmor_v1.SdpBasicConfig.SdpBasicConfigEnforcement.ENABLED
                )
            ),
        ),
        # Add template metadata to the template.
        # For more details on template metadata, please refer to the following doc:
        # https://cloud.google.com/security-command-center/docs/reference/model-armor/rest/v1/projects.locations.templates#templatemetadata
        template_metadata=modelarmor_v1.Template.TemplateMetadata(
            ignore_partial_invocation_failures=True, log_sanitize_operations=True
        ),
    )

    # Prepare the request to update the template.
    updated_template = modelarmor_v1.UpdateTemplateRequest(template=template)

    # Update the template.
    response = client.update_template(request=updated_template)

    print(f"Updated Model Armor Template: {response.name}")

    # [END modelarmor_update_template_metadata]

    return response
