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


# [START kms_create_key_asymmetric_sign]
def create_key_asymmetric_sign(project_id, location_id, key_ring_id, id):
    """
    Creates a new asymmetric signing key in Cloud KMS.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        id (string): ID of the key to create (e.g. 'my-asymmetric-signing-key').

    Returns:
        CryptoKey: Cloud KMS key.

    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the parent key ring name.
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)

    # Build the key.
    purpose = kms.enums.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
    algorithm = kms.enums.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PKCS1_2048_SHA256
    key = {
        'purpose': purpose,
        'version_template': {
            'algorithm': algorithm,
        }
    }

    # Call the API.
    created_key = client.create_crypto_key(key_ring_name, id, key)
    print('Created asymmetric signing key: {}'.format(created_key.name))
    return created_key
# [END kms_create_key_asymmetric_sign]
