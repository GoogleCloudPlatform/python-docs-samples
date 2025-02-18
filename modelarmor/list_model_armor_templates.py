# python-docs-samples/modelarmor/list_model_armor_templates.py

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

from typing import List

def list_model_armor_templates(project_id: str, location_id: str) -> List[str]:
    """
    Lists all model armor templates in the specified project and location.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Google Cloud location.

    Returns:
        List[str]: A list of template names.
    """
    from google.cloud import modelarmor_v1
    from google.api_core.client_options import ClientOptions

    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )
    parent = f"projects/{project_id}/locations/{location_id}"
    
    templates = client.list_templates(parent=parent)
    
    templates_name = [template.name for template in templates]
    print(f"Templates Found: {', '.join(template_name for template_name in templates_name)}")
    
    return templates

if __name__ == "__main__":
    # Sample usage
    project_id = "gma-api-53286"
    location_id = "us-central1"

    # Call the function to list templates
    list_model_armor_templates(project_id, location_id)