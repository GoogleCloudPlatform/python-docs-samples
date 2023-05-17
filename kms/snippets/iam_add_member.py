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

from google.iam.v1 import policy_pb2 as iam_policy


# [START kms_iam_add_member]
def iam_add_member(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, member: str
) -> iam_policy.Policy:
    """
    Add an IAM member to a resource.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        member (string): Member to add (e.g. 'user:foo@example.com')

    Returns:
        Policy: Updated Cloud IAM policy.

    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the resource name.
    resource_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # The resource name could also be a key ring.
    # resource_name = client.key_ring_path(project_id, location_id, key_ring_id);

    # Get the current policy.
    policy = client.get_iam_policy(request={"resource": resource_name})

    # Add the member to the policy.
    policy.bindings.add(
        role="roles/cloudkms.cryptoKeyEncrypterDecrypter", members=[member]
    )

    # Save the updated IAM policy.
    request = {"resource": resource_name, "policy": policy}

    updated_policy = client.set_iam_policy(request=request)
    print(f"Added {member} to {resource_name}")
    return updated_policy


# [END kms_iam_add_member]
