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


# [START kms_iam_get_policy]
def iam_get_policy(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> kms.Policy:
    """
    Get the IAM policy for a resource.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').

    Returns:
        Policy: Cloud IAM policy.

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

    # Print the policy
    print(f"IAM policy for {resource_name}")
    for binding in policy.bindings:
        print(binding.role)
        for member in binding.members:
            print(f"- {member}")

    return policy


# [END kms_iam_get_policy]
