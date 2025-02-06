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


def update_model_armor_template(project_id: str, location: str, template_id: str):
    # [START modelarmor_update_template]

    from google.cloud import modelarmor_v1
    client = modelarmor_v1.ModelArmorClient(transport="rest", client_options={
        "api_endpoint": "modelarmor.us-central1.rep.googleapis.com"})

    # TODO(Developer): Uncomment these variables and initialize
    # project_id = "your-google-cloud-project-id"
    # location = "us-central1"
    # template_id = "template_id"

    updated_template = {
        "name": f"projects/{project_id}/locations/{location}/templates/{template_id}",
        "filter_config": {
            "rai_settings": {
                "rai_filters": [
                    {
                        "filter_type": "HATE_SPEECH",
                        "confidence_level": "MEDIUM_AND_ABOVE"
                    },
                ]
            },
        },
        "template_metadata": {
            "log_template_operations": True,
            "log_sanitize_operations": True
        }

    }

    # Initialize request argument(s)
    request = modelarmor_v1.UpdateTemplateRequest(
        template=updated_template
    )

    # Make the request
    response = client.update_template(request=request)

    # Response
    return response
# [END modelarmor_update_template]