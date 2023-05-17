# Copyright 2023 Google LLC
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


# [START kms_get_public_key_jwk]
def get_public_key_jwk(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str
) -> kms.PublicKey:
    """
    Get the public key of an asymmetric key in JWK format.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        version_id (string): ID of the key to use (e.g. '1').

    Returns:
        PublicKey: Cloud KMS public key response.

    """

    # Import the client library.
    from google.cloud import kms
    from jwcrypto import jwk

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key version name.
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Call the API.
    public_key = client.get_public_key(request={"name": key_version_name})

    # Optional, but recommended: perform integrity verification on public_key.
    # For more details on ensuring E2E in-transit integrity to and from Cloud KMS visit:
    # https://cloud.google.com/kms/docs/data-integrity-guidelines
    if not public_key.name == key_version_name:
        raise Exception("The request sent to the server was corrupted in-transit.")
    # See crc32c() function defined below.
    if not public_key.pem_crc32c == crc32c(public_key.pem):
        raise Exception(
            "The response received from the server was corrupted in-transit."
        )
    # End integrity verification

    # Convert to JWK format.
    jwk = jwk.JWK.from_pem(public_key.pem.encode())
    return jwk.export(private_key=False)


def crc32c(data: bytes) -> int:
    """
    Calculates the CRC32C checksum of the provided data.
    Args:
        data: the bytes over which the checksum should be calculated.
    Returns:
        An int representing the CRC32C checksum of the provided bytes.
    """
    import crcmod  # type: ignore
    import six  # type: ignore

    crc32c_fun = crcmod.predefined.mkPredefinedCrcFun("crc-32c")
    return crc32c_fun(six.ensure_binary(data))


# [END kms_get_public_key_jwk]
