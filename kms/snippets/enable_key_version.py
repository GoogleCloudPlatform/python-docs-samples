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


# [START kms_enable_key_version]
def enable_key_version(project_id, location_id, key_ring_id, key_id, version_id):
    """
    Enable a key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        version_id (string): ID of the key version to enable (e.g. '1').

    Returns:
        CryptoKeyVersion: The version.

    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key version name.
    key_version_name = client.crypto_key_version_path(project_id, location_id, key_ring_id, key_id, version_id)

    key_version = {
        'name': key_version_name,
        'state': kms.CryptoKeyVersion.CryptoKeyVersionState.ENABLED
    }

    # Build the update mask.
    update_mask = {'paths': ['state']}

    # Call the API.
    enabled_version = client.update_crypto_key_version(request={'crypto_key_version': key_version, 'update_mask': update_mask})
    print('Enabled key version: {}'.format(enabled_version.name))
    return enabled_version
# [END kms_enable_key_version]
