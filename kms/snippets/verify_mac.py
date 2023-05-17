# Copyright 2021 Google LLC
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


# [START kms_verify_mac]
def verify_mac(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    version_id: str,
    data: str,
    signature: bytes,
) -> kms.MacVerifyResponse:
    """
    Verify the signature of data from an HMAC key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        version_id (string): Version to use (e.g. '1').
        data (string): Data that was signed.
        signature (bytes): Signature bytes.

    Returns:
        MacVerifyResponse: Success.
    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key version name.
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Convert the message to bytes.
    data_bytes = data.encode("utf-8")

    # Call the API
    verify_response = client.mac_verify(
        request={"name": key_version_name, "data": data_bytes, "mac": signature}
    )

    print(f"Verified: {verify_response.success}")
    return verify_response


# [END kms_verify_mac]
