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


# [START kms_create_key_version]
def create_key_version(project_id, location_id, key_ring_id, key_id):
    """
    Creates a new version of the given key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key for which to create a new version (e.g. 'my-key').

    Returns:
        CryptoKeyVersion: Cloud KMS key version.

    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the parent key name.
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Build the key version.
    version = {}

    # Call the API.
    created_version = client.create_crypto_key_version(request={'parent': key_name, 'crypto_key_version': version})
    print('Created key version: {}'.format(created_version.name))
    return created_version
# [END kms_create_key_version]
