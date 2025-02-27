#!/usr/bin/env python

# Copyright 2025 Google LLC
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
creating a new formatted parameter.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_create_structured_param]
def create_structured_param(
    project_id: str, parameter_id: str, format_type: parametermanager_v1.ParameterFormat
) -> parametermanager_v1.Parameter:
    """
    Creates a parameter in the global location of the specified
    project with specified format using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where
        the parameter is to be created.
        parameter_id (str): The ID to assign to the new parameter.
        This ID must be unique within the project.
        format_type (parametermanager_v1.ParameterFormat): The format type of
        the parameter (UNFORMATTED, YAML, JSON).

    Returns:
        parametermanager_v1.Parameter: An object representing the
        newly created parameter.

    Example:
        create_structured_param(
            "my-project",
            "my-global-parameter",
            parametermanager_v1.ParameterFormat.JSON
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parent project in the global location.
    parent = client.common_location_path(project_id, "global")

    # Define the parameter creation request with the specified format.
    request = parametermanager_v1.CreateParameterRequest(
        parent=parent,
        parameter_id=parameter_id,
        parameter=parametermanager_v1.Parameter(format_=format_type),
    )

    # Create the parameter.
    response = client.create_parameter(request=request)

    # Print the newly created parameter name.
    print(f"Created parameter {response.name} with format {response.format_.name}")
    # [END parametermanager_create_structured_param]

    return response
