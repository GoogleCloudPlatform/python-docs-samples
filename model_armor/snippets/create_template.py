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
Sample code for creating a new model armor template.
"""

from google.cloud import modelarmor_v1


def create_model_armor_template(
    project_id: str,
    location: str,
    template_id: str,
) -> modelarmor_v1.Template:
    """Create a new Model Armor template.

    Args:
        project_id (str): Google Cloud project ID.
        location (str): Google Cloud location.
        template_id (str): ID for the template to create.

    Returns:
        Template: The created template.
    """
    # [START modelarmor_create_template]

    from google.api_core.client_options import ClientOptions
    from google.cloud import modelarmor_v1

    # TODO(Developer): Uncomment these variables.
    # project_id = "your-google-cloud-project-id"
    # location = "us-central1"
    # template_id = "template_id"

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        transport="rest",
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location}.rep.googleapis.com"
        ),
    )

    # Build the Model Armor template with your preferred filters.
    # For more details on filters, please refer to the following doc:
    # https://cloud.google.com/security-command-center/docs/key-concepts-model-armor#ma-filters
    template = modelarmor_v1.Template(
        filter_config=modelarmor_v1.FilterConfig(
            pi_and_jailbreak_filter_settings=modelarmor_v1.PiAndJailbreakFilterSettings(
                filter_enforcement=modelarmor_v1.PiAndJailbreakFilterSettings.PiAndJailbreakFilterEnforcement.ENABLED,
                confidence_level=modelarmor_v1.DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
            ),
            malicious_uri_filter_settings=modelarmor_v1.MaliciousUriFilterSettings(
                filter_enforcement=modelarmor_v1.MaliciousUriFilterSettings.MaliciousUriFilterEnforcement.ENABLED,
            ),
        ),
    )

    # Prepare the request for creating the template.
    request = modelarmor_v1.CreateTemplateRequest(
        parent=f"projects/{project_id}/locations/{location}",
        template_id=template_id,
        template=template,
    )

    # Create the template.
    response = client.create_template(request=request)

    # Print the new template name.
    print(f"Created template: {response.name}")

    # [END modelarmor_create_template]

    return response
