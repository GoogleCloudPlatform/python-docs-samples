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
creating a regional parameter and binding a tag to it.
"""

from google.cloud import resourcemanager_v3


# [START parametermanager_bind_tags_to_regional_param]
def bind_tags_to_regional_param(
    project_id: str, location_id: str, parameter_id: str, tag_value: str
) -> resourcemanager_v3.TagBinding:
    """
    Creates a parameter in the specified region of the specified project and then
    binds an existing tag value to it through the Resource Manager API.

    Args:
        project_id (str): The ID of the project.
        location_id (str): The region where the parameter is located.
        parameter_id (str): The ID to assign to the new parameter.
        tag_value (str): The tag value resource name, e.g. tagValues/1234567890.

    Returns:
        resourcemanager_v3.TagBinding: An object representing the tag binding.

    Example:
        bind_tags_to_regional_param(
            "my-project",
            "us-central1",
            "my-parameter",
            "tagValues/1234567890"
        )
    """
    # Import the necessary libraries.
    from google.cloud import parametermanager_v1
    from google.cloud import resourcemanager_v3

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Create the Resource Manager tag bindings client with the regional endpoint.
    resource_manager_client = resourcemanager_v3.TagBindingsClient(
        client_options={
            "api_endpoint": f"{location_id}-cloudresourcemanager.googleapis.com"
        }
    )

    # Build the resource name of the parent project.
    parent = client.common_location_path(project_id, location_id)

    # Create the parameter.
    parameter = client.create_parameter(
        request={"parent": parent, "parameter_id": parameter_id}
    )

    # Print the new parameter name.
    print(f"Created regional parameter: {parameter.name}")

    # Define the tag binding request for the new parameter.
    request = resourcemanager_v3.CreateTagBindingRequest(
        tag_binding=resourcemanager_v3.TagBinding(
            parent=f"//parametermanager.googleapis.com/{parameter.name}",
            tag_value=tag_value,
        ),
    )

    # Create the tag binding and wait for the operation to complete.
    operation = resource_manager_client.create_tag_binding(request=request)
    response = operation.result()

    # Print the tag binding.
    print(f"Created tag binding: {response.name}")
    # [END parametermanager_bind_tags_to_regional_param]

    return response
