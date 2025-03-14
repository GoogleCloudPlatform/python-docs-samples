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
Sample code for creating a new model armor template with advanced SDP settings
enabled.
"""

from google.cloud import modelarmor_v1


def create_model_armor_template_with_advanced_sdp(
    project_id: str,
    location_id: str,
    template_id: str,
    inspect_template: str,
    deidentify_template: str,
) -> modelarmor_v1.Template:
    """
    Creates a new model armor template with advanced SDP settings enabled.

    Args:
        project_id (str): Google Cloud project ID where the template will be created.
        location_id (str): Google Cloud location where the template will be created.
        template_id (str): ID for the template to create.
        inspect_template (str):
            Optional. Sensitive Data Protection inspect template
            resource name.
            If only inspect template is provided (de-identify template
            not provided), then Sensitive Data Protection InspectContent
            action is performed during Sanitization. All Sensitive Data
            Protection findings identified during inspection will be
            returned as SdpFinding in SdpInsepctionResult e.g.
            `organizations/{organization}/inspectTemplates/{inspect_template}`,
            `projects/{project}/inspectTemplates/{inspect_template}`
            `organizations/{organization}/locations/{location}/inspectTemplates/{inspect_template}`
            `projects/{project}/locations/{location}/inspectTemplates/{inspect_template}`
        deidentify_template (str):
            Optional. Optional Sensitive Data Protection Deidentify
            template resource name.
            If provided then DeidentifyContent action is performed
            during Sanitization using this template and inspect
            template. The De-identified data will be returned in
            SdpDeidentifyResult. Note that all info-types present in the
            deidentify template must be present in inspect template.
            e.g.
            `organizations/{organization}/deidentifyTemplates/{deidentify_template}`,
            `projects/{project}/deidentifyTemplates/{deidentify_template}`
            `organizations/{organization}/locations/{location}/deidentifyTemplates/{deidentify_template}`
            `projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}`
    Example:
        # Create template with advance SDP configuration
        create_model_armor_template_with_advanced_sdp(
            'my_project',
            'us-central1',
            'advance-sdp-template-id',
            'projects/my_project/locations/us-central1/inspectTemplates/inspect_template_id',
            'projects/my_project/locations/us-central1/deidentifyTemplates/de-identify_template_id'
        )

    Returns:
        Template: The created Template.
    """
    # [START modelarmor_create_template_with_advanced_sdp]

    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "YOUR_PROJECT_ID"
    # location_id = "us-central1"
    # template_id = "template_id"
    # inspect_template = f"projects/{project_id}/inspectTemplates/{inspect_template_id}"
    # deidentify_template = f"projects/{project_id}/deidentifyTemplates/{deidentify_template_id}"

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
                advanced_config=modelarmor_v1.SdpAdvancedConfig(
                    inspect_template=inspect_template,
                    deidentify_template=deidentify_template,
                )
            ),
        ),
    )

    # Prepare the request for creating the template.
    create_template = modelarmor_v1.CreateTemplateRequest(
        parent=parent, template_id=template_id, template=template
    )

    # Create the template.
    response = client.create_template(request=create_template)

    # Print the new template name.
    print(f"Created template: {response.name}")

    # [END modelarmor_create_template_with_advanced_sdp]

    return response
