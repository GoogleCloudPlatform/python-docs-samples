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
deleting a parameter.
"""


# [START parametermanager_delete_param]
def delete_param(project_id: str, parameter_id: str) -> None:
    """
    Deletes a parameter from the global location of the specified
    project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project
        where the parameter is located.
        parameter_id (str): The ID of the parameter to delete.

    Returns:
        None

    Example:
        delete_param(
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

    # Delete the parameter.
    client.delete_parameter(name=name)

    # Print confirmation of deletion.
    print(f"Deleted parameter: {name}")
    # [END parametermanager_delete_param]
