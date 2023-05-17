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


# [START kms_encrypt_asymmetric]
def encrypt_asymmetric(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    version_id: str,
    plaintext: str,
) -> bytes:
    """
    Encrypt plaintext using the public key portion of an asymmetric key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        version_id (string): ID of the key version to use (e.g. '1').
        plaintext (string): message to encrypt

    Returns:
        bytes: Encrypted ciphertext.

    """

    # Import the client library.
    from google.cloud import kms

    # Import base64 for printing the ciphertext.
    import base64

    # Import cryptographic helpers from the cryptography package.
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    # Convert the plaintext to bytes.
    plaintext_bytes = plaintext.encode("utf-8")

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key version name.
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Get the public key.
    public_key = client.get_public_key(request={"name": key_version_name})

    # Extract and parse the public key as a PEM-encoded RSA key.
    pem = public_key.pem.encode("utf-8")
    rsa_key = serialization.load_pem_public_key(pem, default_backend())

    # Construct the padding. Note that the padding differs based on key choice.
    sha256 = hashes.SHA256()
    mgf = padding.MGF1(algorithm=sha256)
    pad = padding.OAEP(mgf=mgf, algorithm=sha256, label=None)

    # Encrypt the data using the public key.
    ciphertext = rsa_key.encrypt(plaintext_bytes, pad)
    print(f"Ciphertext: {base64.b64encode(ciphertext)!r}")
    return ciphertext


# [END kms_encrypt_asymmetric]
