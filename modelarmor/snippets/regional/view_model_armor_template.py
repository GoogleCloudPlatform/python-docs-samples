# python-docs-samples/modelarmor/view_model_armor_template.py

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

import argparse
from typing import Dict

# [START view_modelarmor_template]
def view_model_armor_template(project_id: str, location_id: str, template_id: str) -> Dict:
    """
    Retrieves details for a model armor template.

    Args:
        project_id (str): Google Cloud project ID where the template exists.
        location_id (str): Google Cloud location where the template exists.
        template_id (str): ID of the template to view.

    Returns:
        Dict: A dictionary containing the details of the Model Armor Template.
    """
    from google.cloud import modelarmor_v1
    from google.api_core.client_options import ClientOptions

    # Create Model Armor client.
    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )

    # Build the fully qualified name of the template.
    template_name = f"projects/{project_id}/locations/{location_id}/templates/{template_id}"

    # Get the template details using the client.
    template = client.get_template(name=template_name)
    
    # Print the template name and details.
    print(f"Model Armor Template Details: {template}")
    # [END view_modelarmor_template]
    return template

if __name__ == "__main__":
    # Sample usage
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="The project ID where the template exists.")
    parser.add_argument("location_id", help="The location where the template exists.")
    parser.add_argument("template_id", help="The ID of the template to view.")
    
    args = parser.parse_args()

    # Call the function to view template details
    view_model_armor_template(args.project_id, args.location_id, args.template_id)