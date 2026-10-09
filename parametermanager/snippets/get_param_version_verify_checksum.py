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
getting a parameter version and verifying its checksum.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_get_param_version_verify_checksum]
def get_param_version_verify_checksum(
    project_id: str, parameter_id: str, version_id: str
) -> parametermanager_v1.ParameterVersion:
    """
    Gets a parameter version and verifies its payload checksum.

    Args:
        project_id (str): The ID of the project.
        parameter_id (str): The ID of the parameter for which the version
        details are to be retrieved.
        version_id (str): The ID of the parameter version to be retrieved.

    Returns:
        parametermanager_v1.ParameterVersion: An object representing the parameter version.

    Example:
        get_param_version_verify_checksum(
            "my-project",
            "my-parameter",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    import google_crc32c

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parameter version.
    name = client.parameter_version_path(project_id, "global", parameter_id, version_id)

    # Get the parameter version with the payload and checksum (full view).
    request = parametermanager_v1.GetParameterVersionRequest(
        name=name, view=parametermanager_v1.View.FULL
    )
    response = client.get_parameter_version(request=request)

    # Verify the payload checksum.
    computed_crc32c = google_crc32c.value(response.payload.data)
    if computed_crc32c != response.payload.data_crc32c:
        raise ValueError(f"Checksum mismatch for {response.name}: data corrupted")

    # Print the verification result and the checksum source.
    print(f"Verified checksum for parameter version: {response.name}")
    print(f"Checksum source: {response.checksum_source.name}")
    # [END parametermanager_get_param_version_verify_checksum]

    return response
