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


# [START kms_create_key_ring]
def create_key_ring(
    project_id: str, location_id: str, key_ring_id: str, key_id: str
) -> kms.CryptoKey:
    """
    Creates a new key ring in Cloud KMS

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the key ring to create (e.g. 'my-key-ring').

    Returns:
        KeyRing: Cloud KMS key ring.

    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the parent location name.
    location_name = f"projects/{project_id}/locations/{location_id}"

    # Build the key ring.
    key_ring = {}

    # Call the API.
    created_key_ring = client.create_key_ring(
        request={
            "parent": location_name,
            "key_ring_id": key_ring_id,
            "key_ring": key_ring,
        }
    )
    print(f"Created key ring: {created_key_ring.name}")
    return created_key_ring


# [END kms_create_key_ring]
