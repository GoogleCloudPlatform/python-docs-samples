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
creating a new formatted regional parameter version.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_create_structured_regional_param_version]
def create_structured_regional_param_version(
    project_id: str, location_id: str, parameter_id: str, version_id: str, payload: dict
) -> parametermanager_v1.ParameterVersion:
    """
    Creates a new version of an existing parameter in the specified region
    of the specified project using the Google Cloud Parameter Manager SDK.
    The payload is specified as a JSON format.

    Args:
        project_id (str): The ID of the project
        where the parameter is located.
        location_id (str): The ID of the region
        where the parameter is located.
        parameter_id (str): The ID of the parameter for
        which the version is to be created.
        version_id (str): The ID of the version to be created.
        payload (dict): The JSON dictionary payload to be
        stored in the new parameter version.

    Returns:
        parametermanager_v1.ParameterVersion: An object representing the
        newly created parameter version.

    Example:
        create_structured_regional_param_version(
            "my-project",
            "us-central1",
            "my-regional-parameter",
            "v1",
            {"username": "test-user", "host": "localhost"}
        )
    """
    # Import the necessary libraries for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    import json

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parameter.
    parent = client.parameter_path(project_id, location_id, parameter_id)

    # Convert the JSON dictionary to a string and then encode it to bytes.
    payload_bytes = json.dumps(payload).encode("utf-8")

    # Define the parameter version creation request with the JSON payload.
    request = parametermanager_v1.CreateParameterVersionRequest(
        parent=parent,
        parameter_version_id=version_id,
        parameter_version=parametermanager_v1.ParameterVersion(
            payload=parametermanager_v1.ParameterVersionPayload(data=payload_bytes)
        ),
    )

    # Create the parameter version.
    response = client.create_parameter_version(request=request)

    # Print the newly created parameter version name.
    print(f"Created regional parameter version: {response.name}")
    # [END parametermanager_create_structured_regional_param_version]

    return response
