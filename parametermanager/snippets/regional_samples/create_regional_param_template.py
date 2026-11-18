#!/usr/bin/env python

# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
"""
command line application and sample code for
creating a new template.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_create_regional_param_template]
def create_regional_param_template(
    project_id: str,
    location_id: str,
    template_id: str,
    format_type: parametermanager_v1.TemplateFormat,
) -> parametermanager_v1.Template:
    """
    Creates a template in the specified region of the specified project with the
    specified format using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project.
        location_id (str): The region where the resources are located.
        template_id (str): The ID to assign to the new template.
        format_type (parametermanager_v1.TemplateFormat): The format of the
        template (TEMPLATE_FORMAT_YAML or TEMPLATE_FORMAT_JSON).

    Returns:
        parametermanager_v1.Template: An object representing the newly created template.

    Example:
        create_regional_param_template(
            "my-project",
            "us-central1",
            "my-template",
            parametermanager_v1.TemplateFormat.TEMPLATE_FORMAT_JSON
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parent project in the specified region.
    parent = client.common_location_path(project_id, location_id)

    # Define the template creation request with the specified format.
    request = parametermanager_v1.CreateTemplateRequest(
        parent=parent,
        template_id=template_id,
        template=parametermanager_v1.Template(format_=format_type),
    )

    # Create the template.
    response = client.create_template(request=request)

    # Print the newly created template name.
    print(
        f"Created regional template {response.name} with format {response.format_.name}"
    )
    # [END parametermanager_create_regional_param_template]

    return response
