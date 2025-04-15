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
Sample code for getting started with model armor.
"""


def quickstart(
    project_id: str,
    location_id: str,
    template_id: str,
) -> None:
    """
    Creates a new model armor template and sanitize a user prompt using it.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.
        template_id (str): ID for the template to create.
    """
    # [START modelarmor_quickstart]

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
            )
        ),
    )

    # Create a template with Responsible AI Filters.
    client.create_template(
        request=modelarmor_v1.CreateTemplateRequest(
            parent=parent, template_id=template_id, template=template
        )
    )

    # Sanitize a user prompt using the created template.
    user_prompt = "Unsafe user prompt"

    user_prompt_sanitize_response = client.sanitize_user_prompt(
        request=modelarmor_v1.SanitizeUserPromptRequest(
            name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
            user_prompt_data=modelarmor_v1.DataItem(text=user_prompt),
        )
    )

    # Print the detected findings, if any.
    print(
        f"Result for User Prompt Sanitization: {user_prompt_sanitize_response.sanitization_result}"
    )

    # Sanitize a model response using the created template.
    model_response = (
        "Unsanitized model output"
    )

    model_sanitize_response = client.sanitize_model_response(
        request=modelarmor_v1.SanitizeModelResponseRequest(
            name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
            model_response_data=modelarmor_v1.DataItem(text=model_response),
        )
    )

    # Print the detected findings, if any.
    print(
        f"Result for Model Response Sanitization: {model_sanitize_response.sanitization_result}"
    )

    # [END modelarmor_quickstart]
