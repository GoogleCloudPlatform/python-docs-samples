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
deleting a template version.
"""


# [START parametermanager_delete_regional_param_template_version]
def delete_regional_param_template_version(
    project_id: str, location_id: str, template_id: str, version_id: str
) -> None:
    """
    Deletes a specific version of an existing template in the specified region
    of the specified project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project.
        location_id (str): The region where the resources are located.
        template_id (str): The ID of the template whose version is to be
        deleted.
        version_id (str): The ID of the template version to be deleted.

    Returns:
        None

    Example:
        delete_regional_param_template_version(
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

    # Delete the template version.
    client.delete_template_version(request={"name": name})

    # Print confirmation of the deletion.
    print(f"Deleted regional template version: {name}")
    # [END parametermanager_delete_regional_param_template_version]
