# Copyright 2020 Google LLC
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

from google.cloud import kms


# [START kms_destroy_key_version]
def destroy_key_version(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str
) -> kms.CryptoKeyVersion:
    """
    Schedule destruction of the given key version.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        version_id (string): ID of the key version to destroy (e.g. '1').

    Returns:
        CryptoKeyVersion: The version.

    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key version name.
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Call the API.
    destroyed_version = client.destroy_crypto_key_version(
        request={"name": key_version_name}
    )
    print(f"Destroyed key version: {destroyed_version.name}")
    return destroyed_version


# [END kms_destroy_key_version]
