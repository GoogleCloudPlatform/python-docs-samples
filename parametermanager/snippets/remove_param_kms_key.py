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
command line application and sample code for removing the kms key of the parameter.
"""
from google.cloud import parametermanager_v1


# [START parametermanager_remove_param_kms_key]
def remove_param_kms_key(
    project_id: str, parameter_id: str
) -> parametermanager_v1.Parameter:
    """
    Remove a kms key of a specified global parameter
    in the specified project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where the parameter is located.
        parameter_id (str): The ID of the parameter for
        which kms key is to be removed.

    Returns:
        parametermanager_v1.Parameter: An object representing the
        updated parameter.

    Example:
        remove_param_kms_key(
            "my-project",
            "my-global-parameter"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    from google.protobuf import field_mask_pb2

    # Create the Parameter Manager client.
    client = parametermanager_v1.ParameterManagerClient()

    # Build the resource name of the parameter.
    name = client.parameter_path(project_id, "global", parameter_id)

    # Get the current parameter details.
    parameter = client.get_parameter(name=name)

    parameter.kms_key = None

    # Define the update mask for the kms_key field.
    update_mask = field_mask_pb2.FieldMask(paths=["kms_key"])

    # Define the request to update the parameter.
    request = parametermanager_v1.UpdateParameterRequest(
        parameter=parameter, update_mask=update_mask
    )

    # Call the API to update (kms_key) the parameter.
    response = client.update_parameter(request=request)

    # Print the parameter ID that it was disabled.
    print(f"Removed kms key for parameter {parameter_id}")
    # [END parametermanager_remove_param_kms_key]

    return response
