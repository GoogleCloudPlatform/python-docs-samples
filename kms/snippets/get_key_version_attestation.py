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

# [START kms_get_key_version_attestation]
def get_key_version_attestation(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str
) -> kms.KeyOperationAttestation:
    """
    Get an HSM-backend key's attestation.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        version_id (string): ID of the version to use (e.g. '1').

    Returns:
        Attestation: Cloud KMS key attestation.

    """

    # Import the client library.
    from google.cloud import kms

    # Import base64 for printing the attestation.
    import base64

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key version name.
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Call the API.
    version = client.get_crypto_key_version(request={"name": key_version_name})

    # Only HSM keys have an attestation. For other key types, the attestion
    # will be None.
    attestation = version.attestation
    if not attestation:
        raise "no attestation - attestations only exist on HSM keys"

    encoded_attestation = base64.b64encode(attestation.content)
    print(f"Got key attestation: {encoded_attestation!r}")
    return attestation


# [END kms_get_key_version_attestation]
