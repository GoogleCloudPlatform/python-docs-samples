# python-docs-samples/modelarmor/update_model_armor_template.py

# Copyright 2021 Google LLC
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

from typing import Dict

def update_model_armor_template(project_id: str, location_id: str, template_id: str, updated_filter_config_data: Dict) -> str:
    """
    Updates an existing model armor template.

    Args:
        project_id (str): Google Cloud project ID where the template exists.
        location_id (str): Google Cloud location where the template exists.
        template_id (str): ID of the template to update.
        updated_filter_config_data (Dict): Updated configuration for the filter settings of the template.

    Returns:
        str: The updated Template's name.
    """
    from google.cloud import modelarmor_v1
    from google.api_core.client_options import ClientOptions

    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )

    template_name = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    updated_filter_config = modelarmor_v1.FilterConfig(**updated_filter_config_data)

    updated_template = modelarmor_v1.Template(
        name=template_name,
        filter_config=updated_filter_config
    )
    
    response = client.update_template(
        template=updated_template
    )
    print(f"Updated Model Armor Template: {response.name}")
    return response.name

if __name__ == "__main__":
    # Sample usage
    project_id = "gma-api-53286"
    location_id = "us-central1"
    template_id = "test-template1"
    updated_filter_config_data = {
        "rai_settings": {
            "rai_filters": [
                {
                    "filter_type": "HATE_SPEECH",
                    "confidence_level": "HIGH" # changed to high from medium
                }, 
                {
                    "filter_type": "HARASSMENT",
                    "confidence_level": "HIGH"
                }, 
                {
                    "filter_type": "DANGEROUS",
                    "confidence_level": "LOW_AND_ABOVE" # changed to low from medium
                },
                {
                    "filter_type": "SEXUALLY_EXPLICIT",
                    "confidence_level": "MEDIUM_AND_ABOVE"
                }
            ]
        },
        "sdp_settings": {},
        "pi_and_jailbreak_filter_settings": {},
        "malicious_uri_filter_settings": {}
    }

    # Call the function with updated data
    update_model_armor_template(project_id, location_id, template_id, updated_filter_config_data)