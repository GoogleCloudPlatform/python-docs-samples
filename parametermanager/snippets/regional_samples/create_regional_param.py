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
creating a new default format regional parameter.
"""

import argparse

from google.cloud import parametermanager_v1


# [START parametermanager_create_regional_param]
def create_regional_param(
    project_id: str, location_id: str, parameter_id: str
) -> parametermanager_v1.Parameter:
    """
    Creates a regional parameter with default format (Unformatted)
    in the global location of the specified
    project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where
        the parameter is to be created.
        location_id (str): The region where the parameter is to be created.
        parameter_id (str): The ID to assign to the new parameter.
        This ID must be unique within the project.

    Returns:
        parametermanager_v1.Parameter: An object representing
        the newly created parameter.

    Example:
        create_regional_param(
            "my-project",
            "us-central1",
            "my-regional-parameter"
        )
    """

    # Import the Parameter Manager client library.
    from google.cloud import parametermanager_v1

    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    # Create the Parameter Manager client for the specified region.
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parent project for the specified region.
    parent = client.common_location_path(project_id, location_id)

    # Define the parameter creation request.
    request = parametermanager_v1.CreateParameterRequest(
        parent=parent,
        parameter_id=parameter_id,
    )

    # Create the parameter.
    response = client.create_parameter(
        request=request
    )

    # Print the newly created parameter name.
    print(f"Created Regional Parameter: {response.name}")
    # [END parametermanager_create_regional_param]

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument(
        "location_id",
        help="name of the region where the parameter is to be created"
    )
    parser.add_argument("param_id", help="id of the parameter to create")
    args = parser.parse_args()

    create_regional_param(
        args.project_id,
        args.location_id,
        args.param_id
    )
