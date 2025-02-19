
# python-docs-samples/modelarmor/create_model_armor_template_with_advance_sdp.py

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

# [START modelarmor_create_model_armor_template_with_advance_sdp]
def create_model_armor_template(project_id, location_id, template_id, filter_config_data):
    """
    Creates a new model armor template.

    Args:
        project_id (str): Google Cloud project ID where the template will be created.
        location_id (str): Google Cloud location where the template will be created.
        template_id (str): ID for the template to create.
        filter_config (dict): Configuration for the filter settings of the template.

    Returns:
        The created Template's name.
    """
    from google.cloud import modelarmor_v1
    from google.api_core.client_options import ClientOptions

    # Model Armor client creation
    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )
    
    parent = f"projects/{project_id}/locations/{location_id}"
    filter_config = modelarmor_v1.FilterConfig(**filter_config_data)

    template = modelarmor_v1.Template(
        filter_config=filter_config
    )

    # Creat the create template request
    create_template = modelarmor_v1.CreateTemplateRequest(
        parent=parent,
        template_id=template_id,
        template=template
    )

    # Template creation request
    response = client.create_template(
        request=create_template
    )

    print(f"Created Model Armor Template: {response.name}")
    # [END modelarmor_create_model_armor_template_with_advance_sdp]

    return response.name

if __name__ == "__main__":
    # Sample usage
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("project_id", help="GCP project ID")
    parser.add_argument("location_id", help="GCP location")
    parser.add_argument("template_id", help="Template ID")
    parser.add_argument("filter_config_data", help="Filter config data")
    
    args = parser.parse_args()

    # Call the function with sample data
    create_model_armor_template(args.project_id, args.location_id, args.template_id, args.filter_config_data)
