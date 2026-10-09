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


# [START parametermanager_create_param_with_tags]
def create_param_with_tags(
    project_id: str, parameter_id: str, tag_key: str, tag_value: str
) -> parametermanager_v1.Parameter:
    """
    Creates a parameter with a tag.

    Args:
        project_id (str): The ID of the project.
        parameter_id (str): The ID to assign to the new parameter.
        tag_key (str): The tag key resource name, e.g. tagKeys/1234567890.
        tag_value (str): The tag value resource name, e.g. tagValues/1234567890.

    Returns:
        parametermanager_v1.Parameter: An object representing the newly created parameter.

    Example:
        create_param_with_tags(
            "my-project",
            "my-parameter",
            "tagKeys/1234567890",
            "tagValues/1234567890"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parent project in the global location.
    parent = client.common_location_path(project_id, "global")

    # Define the parameter creation request with the tag.
    request = parametermanager_v1.CreateParameterRequest(
        parent=parent,
        parameter_id=parameter_id,
        parameter=parametermanager_v1.Parameter(tags={tag_key: tag_value}),
    )

    # Create the parameter.
    response = client.create_parameter(request=request)

    # Print the newly created parameter name.
    print(f"Created parameter {response.name} with tag {tag_key}: {tag_value}")
    # [END parametermanager_create_param_with_tags]

    return response
