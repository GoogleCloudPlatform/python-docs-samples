#!/usr/bin/env python

# Copyright 2024 Google LLC
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
"""
Command line application and sample code for revoking access to a regional
secret.
"""

import argparse

# [START secretmanager_v1_iam_revoke_access_regional_secret]
# Import the Secret Manager client library.
from google import iam
from google.cloud import secretmanager_v1


def iam_revoke_access_with_regional_secret(
    project_id: str,
    location_id: str,
    secret_id: str,
    member: str,
) -> iam.v1.iam_policy_pb2.SetIamPolicyRequest:
    """
    Revokes the given member access to a secret.
    """

    # Endpoint to call the regional secret manager sever.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret.
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Get the current IAM policy.
    policy = client.get_iam_policy(request={"resource": name})

    # Remove the given member's access permissions.
    accessRole = "roles/secretmanager.secretAccessor"
    for b in list(policy.bindings):
        if b.role == accessRole and member in b.members:
            b.members.remove(member)

    # Update the IAM Policy.
    new_policy = client.set_iam_policy(request={"resource": name, "policy": policy})

    # Print data about the secret.
    print(f"Updated IAM policy on {secret_id}")

    return new_policy


# [END secretmanager_v1_iam_revoke_access_regional_secret]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument("secret_id", help="id of the secret to get")
    parser.add_argument("member", help="member to revoke access")
    args = parser.parse_args()

    iam_revoke_access_with_regional_secret(
        args.project_id, args.location_id, args.secret_id, args.member
    )
