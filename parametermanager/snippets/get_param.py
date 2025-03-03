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
command line application and sample code for getting the parameter details.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_get_param]
def get_param(project_id: str, parameter_id: str) -> parametermanager_v1.Parameter:
    """
    Retrieves a parameter from the global location of the specified
    project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        parameter_id (str): The ID of the parameter to retrieve.

    Returns:
        parametermanager_v1.Parameter: An object representing the parameter.

    Example:
        get_param(
            "my-project",
            "my-global-parameter"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parameter.
    name = client.parameter_path(project_id, "global", parameter_id)

    # Retrieve the parameter.
    parameter = client.get_parameter(name=name)

    # Show parameter details.
    # Find more details for the Parameter object here:
    # https://cloud.google.com/secret-manager/parameter-manager/docs/reference/rest/v1/projects.locations.parameters#Parameter
    print(f"Found the parameter {parameter.name} with format {parameter.format_.name}")
    # [END parametermanager_get_param]

    return parameter
