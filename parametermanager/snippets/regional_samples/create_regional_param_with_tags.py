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
creating a new parameter with tags.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_create_regional_param_with_tags]
def create_regional_param_with_tags(
    project_id: str, location_id: str, parameter_id: str, tag_key: str, tag_value: str
) -> parametermanager_v1.Parameter:
    """
    Creates a parameter with a tag in the specified region of the specified
    project using the Google Cloud Parameter Manager SDK. Tags can only be set
    when the parameter is created. They are not returned when the parameter is
    retrieved. To view a tag binding, use the Resource Manager API.

    Args:
        project_id (str): The ID of the project.
        location_id (str): The region where the resources are located.
        parameter_id (str): The ID to assign to the new parameter.
        tag_key (str): The tag key resource name, e.g. tagKeys/1234567890.
        tag_value (str): The tag value resource name, e.g. tagValues/1234567890.

    Returns:
        parametermanager_v1.Parameter: An object representing the newly created parameter.

    Example:
        create_regional_param_with_tags(
            "my-project",
            "us-central1",
            "my-parameter",
            "tagKeys/1234567890",
            "tagValues/1234567890"
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

    # Define the parameter creation request with the tag.
    request = parametermanager_v1.CreateParameterRequest(
        parent=parent,
        parameter_id=parameter_id,
        parameter=parametermanager_v1.Parameter(tags={tag_key: tag_value}),
    )

    # Create the parameter.
    response = client.create_parameter(request=request)

    # Print the newly created parameter name.
    print(f"Created regional parameter {response.name} with tag {tag_key}: {tag_value}")
    # [END parametermanager_create_regional_param_with_tags]

    return response
