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
command line application and sample code for get the regional parameter details.
"""

import argparse

from google.cloud import parametermanager_v1


# [START parametermanager_get_regional_param]
def get_regional_param(
    project_id: str, location_id: str, parameter_id: str
) -> parametermanager_v1.Parameter:
    """
    Retrieves a parameter from the specified region of the specified
    project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        location_id (str): The ID of the region where the parameter is located.
        parameter_id (str): The ID of the parameter to retrieve.

    Returns:
        parametermanager_v1.Parameter: An object representing the parameter.

    Example:
        get_regional_param(
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

    # Retrieve the parameter.
    parameter = client.get_parameter(name=name)

    # Print the retrieved parameter details.
    print(f"Fetched the Regional Parameter {parameter.name}")
    print(parameter)
    # [END parametermanager_get_regional_param]

    return parameter


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

    get_regional_param(
        args.project_id,
        args.location_id,
        args.param_id
    )
