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
Sample code for deleting a model armor template.
"""


def delete_model_armor_template(
    project_id: str,
    location: str,
    template_id: str,
) -> None:
    """Delete a model armor template.

    Args:
        project_id (str): Google Cloud project ID.
        location (str): Google Cloud location.
        template_id (str): ID for the template to be deleted.
    """
    # [START modelarmor_delete_template]

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

    # Build the request for deleting the template.
    request = modelarmor_v1.DeleteTemplateRequest(
        name=f"projects/{project_id}/locations/{location}/templates/{template_id}",
    )

    # Delete the template.
    client.delete_template(request=request)

    # [END modelarmor_delete_template]
