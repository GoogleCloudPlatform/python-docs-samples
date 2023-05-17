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


# [START kms_verify_asymmetric_signature_ec]
def verify_asymmetric_ec(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    version_id: str,
    message: str,
    signature: str,
) -> bool:
    """
    Verify the signature of an message signed with an asymmetric EC key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        version_id (string): ID of the version to use (e.g. '1').
        message (string): Original message (e.g. 'my message')
        signature (bytes): Signature from a sign request.

    Returns:
        bool: True if verified, False otherwise

    """

    # Import the client library.
    from google.cloud import kms

    # Import cryptographic helpers from the cryptography package.
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec, utils

    # Import hashlib.
    import hashlib

    # Convert the message to bytes.
    message_bytes = message.encode("utf-8")

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key version name.
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Get the public key.
    public_key = client.get_public_key(request={"name": key_version_name})

    # Extract and parse the public key as a PEM-encoded EC key.
    pem = public_key.pem.encode("utf-8")
    ec_key = serialization.load_pem_public_key(pem, default_backend())
    hash_ = hashlib.sha256(message_bytes).digest()

    # Attempt to verify.
    try:
        sha256 = hashes.SHA256()
        ec_key.verify(signature, hash_, ec.ECDSA(utils.Prehashed(sha256)))
        print("Signature verified")
        return True
    except InvalidSignature:
        print("Signature failed to verify")
        return False


# [END kms_verify_asymmetric_signature_ec]
