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
enabling a regional parameter version..
"""

from google.cloud import parametermanager_v1


# [START parametermanager_enable_regional_param_version]
def enable_regional_param_version(
    project_id: str, location_id: str, parameter_id: str, version_id: str
) -> parametermanager_v1.ParameterVersion:
    """
    Enables a regional parameter version in the given project.

    Args:
        project_id (str): The ID of the GCP project
        where the parameter is located.
        location_id (str): The region where the parameter is stored.
        parameter_id (str): The ID of the parameter for
        which version is to be enabled.
        version_id (str): The version ID of the parameter to be enabled.

    Returns:
        parametermanager_v1.ParameterVersion: An object representing the
        enabled parameter version.

    Example:
        enable_regional_param_version(
            "my-project",
            "us-central1",
            "my-regional-parameter",
            "v1"
        )
    """

    # Import the Parameter Manager client library.
    from google.cloud import parametermanager_v1
    from google.protobuf import field_mask_pb2

    # Endpoint to call the regional parameter manager server.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"

    # Create the Parameter Manager client for the specified region.
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the parameter version for the specified region.
    name = client.parameter_version_path(
        project_id, location_id, parameter_id, version_id
    )

    # Get the current parameter version to update its state.
    parameter_version = client.get_parameter_version(request={"name": name})

    # Enable the parameter version.
    parameter_version.disabled = False

    # Create a field mask to specify which fields to update.
    update_mask = field_mask_pb2.FieldMask(paths=["disabled"])

    # Define the parameter version update request.
    request = parametermanager_v1.UpdateParameterVersionRequest(
        parameter_version=parameter_version,
        update_mask=update_mask,
    )

    # Update the parameter version.
    response = client.update_parameter_version(request=request)

    # Print the parameter version ID that it was enabled.
    print(
        f"Enabled regional parameter version {version_id} "
        f"for regional parameter {parameter_id}"
    )
    # [END parametermanager_enable_regional_param_version]

    return response
