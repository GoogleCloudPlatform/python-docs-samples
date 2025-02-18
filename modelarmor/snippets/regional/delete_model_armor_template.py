# python-docs-samples/modelarmor/delete_model_armor_template.py

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


def delete_model_armor_template(project_id: str, location_id: str, template_id: str) -> None:
    """
    Deletes a model armor template.

    Args:
        project_id (str): Google Cloud project ID where the template exists.
        location_id (str): Google Cloud location where the template exists.
        template_id (str): ID of the template to delete.
    """
    from google.cloud import modelarmor_v1
    from google.api_core.client_options import ClientOptions

    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )

    template_name = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    
    client.delete_template(name=template_name)
    
    print(f"Model Armor Template '{template_id}' has been deleted.")

if __name__ == "__main__":
    # Sample usage
    project_id = "gma-api-53286"
    location_id = "us-central1"
    template_id = "test-template-sdp-basic"

    # Call the function to delete the template
    delete_model_armor_template(project_id, location_id, template_id)