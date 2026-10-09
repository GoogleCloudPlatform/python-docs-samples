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
getting a template version.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_get_regional_param_template_version]
def get_regional_param_template_version(
    project_id: str, location_id: str, template_id: str, version_id: str
) -> parametermanager_v1.TemplateVersion:
    """
    Retrieves the details of a specific version of an existing template in the
    specified region of the specified project using the Google Cloud Parameter
    Manager SDK.

    Args:
        project_id (str): The ID of the project.
        location_id (str): The region where the resources are located.
        template_id (str): The ID of the template for which the version details
        are to be retrieved.
        version_id (str): The ID of the template version to be retrieved.

    Returns:
        parametermanager_v1.TemplateVersion: An object representing the template version.

    Example:
        get_regional_param_template_version(
            "my-project",
            "us-central1",
            "my-template",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the template version.
    name = client.template_version_path(
        project_id, location_id, template_id, version_id
    )

    # Get the template version.
    response = client.get_template_version(request={"name": name})

    # Print the template version details.
    print(f"Got regional template version {response.name}")
    print(f"Payload: {response.payload.data.decode('utf-8')}")
    # [END parametermanager_get_regional_param_template_version]

    return response
