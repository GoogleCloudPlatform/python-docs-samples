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


# [START kms_update_key_remove_rotation_schedule]
def update_key_remove_rotation(project_id, location_id, key_ring_id, key_id):
    """
    Remove a rotation schedule from an existing key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').

    Returns:
        CryptoKey: Updated Cloud KMS key.

    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key name.
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    key = {
        'name': key_name
    }

    # Build the update mask.
    update_mask = {'paths': ['rotation_period', 'next_rotation_time']}

    # Call the API.
    updated_key = client.update_crypto_key(request={'crypto_key': key, 'update_mask': update_mask})
    print('Updated key: {}'.format(updated_key.name))
    return updated_key
# [END kms_update_key_remove_rotation_schedule]
