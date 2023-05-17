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


# [START kms_import_manually_wrapped_key]
def import_manually_wrapped_key(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    crypto_key_id: str,
    import_job_id: str,
) -> None:
    """
    Generates and imports local key material to Cloud KMS.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        crypto_key_id (string): ID of the key to import (e.g. 'my-asymmetric-signing-key').
        import_job_id (string): ID of the import job (e.g. 'my-import-job').
    """

    # Import the client library and Python standard cryptographic libraries.
    import os
    from cryptography.hazmat import backends
    from cryptography.hazmat.primitives import hashes, keywrap, serialization
    from cryptography.hazmat.primitives.asymmetric import ec, padding
    from google.cloud import kms

    # Generate some key material in Python and format it in PKCS #8 DER as
    # required by Google Cloud KMS.
    key = ec.generate_private_key(ec.SECP256R1, backends.default_backend())
    formatted_key = key.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )

    print(f"Generated key bytes: {formatted_key!r}")

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Retrieve the fully-qualified crypto_key and import_job string.
    crypto_key_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, crypto_key_id
    )
    import_job_name = client.import_job_path(
        project_id, location_id, key_ring_id, import_job_id
    )

    # Generate a temporary 32-byte key for AES-KWP and wrap the key material.
    kwp_key = os.urandom(32)
    wrapped_target_key = keywrap.aes_key_wrap_with_padding(
        kwp_key, formatted_key, backends.default_backend()
    )

    # Retrieve the public key from the import job.
    import_job = client.get_import_job(name=import_job_name)
    import_job_pub = serialization.load_pem_public_key(
        bytes(import_job.public_key.pem, "UTF-8"), backends.default_backend()
    )

    # Wrap the KWP key using the import job key.
    wrapped_kwp_key = import_job_pub.encrypt(
        kwp_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )

    # Import the wrapped key material.
    client.import_crypto_key_version(
        {
            "parent": crypto_key_name,
            "import_job": import_job_name,
            "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.EC_SIGN_P256_SHA256,
            "rsa_aes_wrapped_key": wrapped_kwp_key + wrapped_target_key,
        }
    )

    print(f"Imported: {import_job.name}")


# [END kms_import_manually_wrapped_key]
