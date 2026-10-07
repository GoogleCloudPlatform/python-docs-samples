#!/usr/bin/env python

# Copyright 2026 Google LLC
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
creating a new parameter version with a checksum.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_create_regional_param_version_with_checksum]
def create_regional_param_version_with_checksum(
    project_id: str, location_id: str, parameter_id: str, version_id: str
) -> parametermanager_v1.ParameterVersion:
    """
    Creates a new version of an existing parameter in the specified region of
    the specified project, sending a CRC32C checksum of the payload so that the
    server can verify the data it received, using the Google Cloud Parameter
    Manager SDK.

    Args:
        project_id (str): The ID of the project.
        location_id (str): The region where the resources are located.
        parameter_id (str): The ID of the parameter for which the version is to
        be created.
        version_id (str): The ID of the parameter version to be created.

    Returns:
        parametermanager_v1.ParameterVersion: An object representing the newly created
        parameter version.

    Example:
        create_regional_param_version_with_checksum(
            "my-project",
            "us-central1",
            "my-parameter",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    import google_crc32c

    # Create the Parameter Manager client with the regional endpoint.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parameter.
    parent = client.parameter_path(project_id, location_id, parameter_id)

    # Define the payload and compute its CRC32C checksum (Castagnoli).
    payload_data = b"hello world!"
    data_crc32c = google_crc32c.value(payload_data)

    # Define the parameter version creation request with the checksum.
    request = parametermanager_v1.CreateParameterVersionRequest(
        parent=parent,
        parameter_version_id=version_id,
        parameter_version=parametermanager_v1.ParameterVersion(
            payload=parametermanager_v1.ParameterVersionPayload(
                data=payload_data, data_crc32c=data_crc32c
            )
        ),
    )

    # Create the parameter version. The request fails with a
    # CHECKSUM_MISMATCH error if the checksum does not match the payload.
    response = client.create_parameter_version(request=request)

    # Print the newly created parameter version name and checksum source.
    print(f"Created regional parameter version: {response.name}")
    print(f"Checksum source: {response.checksum_source.name}")
    # [END parametermanager_create_regional_param_version_with_checksum]

    return response
