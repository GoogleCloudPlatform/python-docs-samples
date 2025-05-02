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
command line application and sample code for updating the kms key of the regional parameter.
"""

from google.cloud import parametermanager_v1


# [START parametermanager_update_regional_param_kms_key]
def update_regional_param_kms_key(
    project_id: str, location_id: str, parameter_id: str, kms_key: str
) -> parametermanager_v1.Parameter:
    """
    Update the kms key of a specified regional parameter
    in the specified project using the Google Cloud Parameter Manager SDK.

    Args:
        project_id (str): The ID of the project where the parameter is to be created.
        location_id (str): The region where the parameter is to be created.
        parameter_id (str): The ID of the regional parameter for
        which kms key is to be updated.
        kms_key (str): The kms_key to be updated for the parameter.

    Returns:
        parametermanager_v1.Parameter: An object representing the
        updated regional parameter.

    Example:
        update_regional_param_kms_key(
            "my-project",
            "us-central1",
            "my-global-parameter",
            "projects/my-project/locations/us-central1/keyRings/test/cryptoKeys/updated-test-key"
        )
    """
    # Import the necessary library for Google Cloud Parameter Manager.
    from google.cloud import parametermanager_v1
    from google.protobuf import field_mask_pb2

    # Create the Parameter Manager client.
    api_endpoint = f"parametermanager.{location_id}.rep.googleapis.com"
    # Create the Parameter Manager client for the specified region.
    client = parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Build the resource name of the regional parameter.
    name = client.parameter_path(project_id, location_id, parameter_id)

    # Get the current regional parameter details.
    parameter = client.get_parameter(name=name)

    # Set the kms key field of the regional parameter.
    parameter.kms_key = kms_key

    # Define the update mask for the kms_key field.
    update_mask = field_mask_pb2.FieldMask(paths=["kms_key"])

    # Define the request to update the parameter.
    request = parametermanager_v1.UpdateParameterRequest(
        parameter=parameter, update_mask=update_mask
    )

    # Call the API to update (kms_key) the parameter.
    response = client.update_parameter(request=request)

    # Print the parameter ID that was updated.
    print(f"Updated regional parameter {parameter_id} with kms key {response.kms_key}")
    # [END parametermanager_update_regional_param_kms_key]

    return response
