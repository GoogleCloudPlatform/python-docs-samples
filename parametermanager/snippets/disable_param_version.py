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
command line application and sample code for disabling the parameter version.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_disable_param_version]
def disable_param_version(
    project_id: str, parameter_id: str, version_id: str
) -> parametermanager_v1.ParameterVersion:
    """
    Disables a specific version of a specified global parameter
    in the specified project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        parameter_id (str): The ID of the parameter for
        which version is to be disabled.
        version_id (str): The ID of the version to be disabled.

    Returns:
        parametermanager_v1.ParameterVersion: An object representing the
        disabled parameter version.

    Example:
        disable_param_version(
            "my-project",
            "my-global-parameter",
            "v1"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    from google.protobuf import field_mask_pb2

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parameter version.
    name = client.parameter_version_path(project_id, "global", parameter_id, version_id)

    # Get the current parameter version details.
    parameter_version = client.get_parameter_version(name=name)

    # Set the disabled field to True to disable the version.
    parameter_version.disabled = True

    # Define the update mask for the disabled field.
    update_mask = field_mask_pb2.FieldMask(paths=["disabled"])

    # Define the request to update the parameter version.
    request = parametermanager_v1.UpdateParameterVersionRequest(
        parameter_version=parameter_version, update_mask=update_mask
    )

    # Call the API to update (disable) the parameter version.
    response = client.update_parameter_version(request=request)

    # Print the parameter version ID that it was disabled.
    print(f"Disabled parameter version {version_id} for parameter {parameter_id}")
    # [END parametermanager_disable_param_version]

    return response
