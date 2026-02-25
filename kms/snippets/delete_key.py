# Copyright 2026 Google LLC
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
# limitations under the License.

# [START kms_delete_key]
from google.cloud import kms


def delete_key(
    project_id: str, location_id: str, key_ring_id: str, key_id: str
) -> None:
    """
    Delete the given key. This action is permanent and cannot be undone. Once the
    key is deleted, it will no longer exist.

    Args:
        project_id (str): Google Cloud project ID (e.g. 'my-project').
        location_id (str): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (str): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (str): ID of the key to use (e.g. 'my-key').

    Returns:
        None

    """

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key name.
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Call the API.
    # Note: delete_crypto_key returns a long-running operation.
    # Warning: This operation is permanent and cannot be undone.
    operation = client.delete_crypto_key(request={"name": key_name})

    # Wait for the operation to complete.
    operation.result()

    print(f"Deleted key: {key_name}")


# [END kms_delete_key]
