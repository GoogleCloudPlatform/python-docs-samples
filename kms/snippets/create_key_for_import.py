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


# [START kms_create_key_for_import]
def create_key_for_import(project_id, location_id, key_ring_id, crypto_key_id):
    """

    Sets up an empty CryptoKey within a KeyRing for import.


    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        crypto_key_id (string): ID of the key to import (e.g. 'my-asymmetric-signing-key').
    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key. For more information regarding allowed values of these fields, see:
    # https://googleapis.dev/python/cloudkms/latest/_modules/google/cloud/kms_v1/types/resources.html
    purpose = kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
    algorithm = kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.EC_SIGN_P256_SHA256
    protection_level = kms.ProtectionLevel.HSM
    key = {
        'purpose': purpose,
        'version_template': {
            'algorithm': algorithm,
            'protection_level': protection_level
        }
    }

    # Build the parent key ring name.
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)

    # Call the API.
    created_key = client.create_crypto_key(request={'parent': key_ring_name, 'crypto_key_id': crypto_key_id, 'crypto_key': key})
    print('Created hsm key: {}'.format(created_key.name))
# [END kms_create_key_for_import]
