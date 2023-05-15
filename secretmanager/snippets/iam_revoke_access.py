#!/usr/bin/env python

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
"""
command line application and sample code for revoking access to a secret.
"""

import argparse


# [START secretmanager_iam_revoke_access]
def iam_revoke_access(project_id, secret_id, member):
    """
    Revoke the given member access to a secret.
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

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
    # [END secretmanager_iam_revoke_access]

    return new_policy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to get")
    parser.add_argument("member", help="member to revoke access")
    args = parser.parse_args()

    iam_revoke_access(args.project_id, args.secret_id, args.member)
