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
creating a regional parameter version with secret reference.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_create_regional_param_version_with_secret]
def create_regional_param_version_with_secret(
    project_id: str,
    location_id: str,
    parameter_id: str,
    version_id: str,
    secret_id: str,
) -> parametermanager_v1.ParameterVersion:
    """
    Creates a new version of an existing parameter in the specified region
    of the specified project using the Google Cloud Parameter Manager SDK.
    The payload is specified as a JSON string and
    includes a reference to a secret.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        location_id (str): The ID of the region where the parameter is located.
        parameter_id (str): The ID of the parameter for
        which the version is to be created.
        version_id (str): The ID of the version to be created.
        secret_id (str): The ID of the secret to be referenced.

    Returns:
        parametermanager_v1.ParameterVersion: An object representing the
        newly created parameter version.

    Example:
        create_regional_param_version_with_secret(
            "my-project",
            "us-central1",
            "my-regional-parameter",
            "v1",
            "projects/my-project/locations/us-central1/
            secrets/application-secret/version/latest"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    import json

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parameter.
    parent = client.parameter_path(project_id, location_id, parameter_id)

    # Create the JSON payload with a secret reference.
    payload_dict = {
        "username": "test-user",
        "password": f"__REF__('//secretmanager.googleapis.com/{secret_id}')",
    }
    payload_json = json.dumps(payload_dict)

    # Define the parameter version creation request with the JSON payload.
    request = parametermanager_v1.CreateParameterVersionRequest(
        parent=parent,
        parameter_version_id=version_id,
        parameter_version=parametermanager_v1.ParameterVersion(
            payload=parametermanager_v1.ParameterVersionPayload(
                data=payload_json.encode("utf-8")
            )
        ),
    )

    # Create the parameter version.
    response = client.create_parameter_version(request=request)

    # Print the newly created parameter version name.
    print(f"Created regional parameter version: {response.name}")
    # [END parametermanager_create_regional_param_version_with_secret]

    return response
