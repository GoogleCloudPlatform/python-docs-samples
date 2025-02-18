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
creating unformatted regional parameter version.
"""

import argparse

from google.cloud import parametermanager_v1


# [START parametermanager_create_regional_param_version]
def create_regional_param_version(
    project_id: str, location_id: str,
    parameter_id: str, version_id: str, payload: str
) -> parametermanager_v1.ParameterVersion:
    """
    Creates a new version of an existing parameter in the specified region
    of the specified project using the Google Cloud Parameter Manager SDK.
    The payload is specified as an unformatted string.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        location_id (str): The ID of the region where the parameter is located.
        parameter_id (str): The ID of the parameter for which
        the version is to be created.
        version_id (str): The ID of the version to be created.
        payload (str): The unformatted string payload
        to be stored in the new parameter version.

    Returns:
        parametermanager_v1.ParameterVersion: An object representing the
        newly created parameter version.

    Example:
        create_regional_param_version(
            "my-project",
            "us-central1",
            "my-regional-parameter",
            "v1",
            "my-unformatted-payload"
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
    parent = client.parameter_path(project_id, location_id, parameter_id)

    # Define the parameter version creation request with an unformatted payload.
    request = parametermanager_v1.CreateParameterVersionRequest(
        parent=parent,
        parameter_version_id=version_id,
        parameter_version=parametermanager_v1.ParameterVersion(
            payload=parametermanager_v1.ParameterVersionPayload(
                data=payload.encode("utf-8")  # Encoding the payload to bytes.
            )
        )
    )

    # Create the parameter version.
    response = client.create_parameter_version(request=request)

    # Print the newly created parameter version name.
    print(f"Created Regional Parameter Version: {response.name}")
    # [END parametermanager_create_regional_param_version]

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
    parser.add_argument(
        "version_id",
        help="id of the version of the parameter to create"
    )
    args = parser.parse_args()

    create_regional_param_version(
        args.project_id,
        args.location_id,
        args.param_id,
        args.version_id,
        "my-unformatted-payload"
    )
