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
command line application and sample code for listing regional parameters.
"""


# [START parametermanager_list_regional_params]
def list_regional_params(project_id: str, location_id: str) -> None:
    """
    Lists all parameters in the specified region for the specified
    project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where
        the parameters are located.
        location_id (str): The ID of the region where
        the parameters are located.

    Returns:
        None

    Example:
        list_regional_params(
            "my-project",
            "us-central1"
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

    # List all parameters in the specified parent project and region.
    for parameter in client.list_parameters(parent=parent):
        print(f"Found regional parameter {parameter.name} with format {parameter.format_.name}")

    # [END parametermanager_list_regional_params]
