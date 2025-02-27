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
quickstart with regional parameter manager.
"""


# [START parametermanager_regional_quickstart]
def regional_quickstart(
    project_id: str, location_id: str, parameter_id: str, version_id: str
) -> None:
    """
    Quickstart example for using Google Cloud Parameter Manager to
    create a regional parameter, add a version with a JSON payload,
    and fetch the parameter version details.

    Args:
        project_id (str): The ID of the GCP project
        where the parameter is to be created.
        location_id (str): The region where the parameter is to be created.
        parameter_id (str): The ID to assign to the new parameter.
        version_id (str): The ID of the parameter version.

    Returns:
        None

    Example:
        regional_quickstart(
            "my-project",
            "us-central1",
            "my-regional-parameter",
            "v1"
        )
    """

    # Import necessary libraries
    from google.cloud import parametermanager_v1
    import json

    # Set the API endpoint for the specified region
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"

    # Create the Parameter Manager client for the specified region
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parent project for the specified region
    parent = client.common_location_path(project_id, location_id)

    # Define the parameter creation request with JSON format
    parameter = parametermanager_v1.Parameter(
        format_=parametermanager_v1.ParameterFormat.JSON
    )
    create_param_request = parametermanager_v1.CreateParameterRequest(
        parent=parent, parameter_id=parameter_id, parameter=parameter
    )

    # Create the parameter
    response = client.create_parameter(request=create_param_request)
    print(
        f"Created regional parameter {response.name} "
        f"with format {response.format_.name}"
    )

    # Define the payload
    payload_data = {"username": "test-user", "host": "localhost"}
    payload = parametermanager_v1.ParameterVersionPayload(
        data=json.dumps(payload_data).encode("utf-8")
    )

    # Define the parameter version creation request
    create_version_request = parametermanager_v1.CreateParameterVersionRequest(
        parent=response.name,
        parameter_version_id=version_id,
        parameter_version=parametermanager_v1.ParameterVersion(payload=payload),
    )

    # Create the parameter version
    version_response = client.create_parameter_version(request=create_version_request)
    print(f"Created regional parameter version: {version_response.name}")

    # Render the parameter version to get the simple and rendered payload
    get_param_request = parametermanager_v1.GetParameterVersionRequest(
        name=version_response.name
    )
    get_param_response = client.get_parameter_version(get_param_request)

    # Print the simple and rendered payload
    payload = get_param_response.payload.data.decode("utf-8")
    print(f"Payload: {payload}")
    # [END parametermanager_regional_quickstart]
