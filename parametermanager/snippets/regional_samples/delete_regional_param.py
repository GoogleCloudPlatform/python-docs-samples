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
deleting a regional parameter.
"""


# [START parametermanager_delete_regional_param]
def delete_regional_param(project_id: str, location_id: str, parameter_id: str) -> None:
    """
    Deletes a parameter from the specified region of the specified
    project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project
        where the parameter is located.
        location_id (str): The ID of the region
        where the parameter is located.
        parameter_id (str): The ID of the parameter to delete.

    Returns:
        None

    Example:
        delete_regional_param(
            "my-project",
            "us-central1",
            "my-regional-parameter"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parameter.
    name = client.parameter_path(project_id, location_id, parameter_id)

    # Delete the parameter.
    client.delete_parameter(name=name)

    # Print confirmation of deletion.
    print(f"Deleted regional parameter: {name}")
    # [END parametermanager_delete_regional_param]
