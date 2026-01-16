#!/usr/bin/env python

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

# [START secretmanager_create_secret_with_cmek]
from google.cloud import secretmanager_v1


def create_secret_with_cmek(
    project_id: str, secret_id: str, kms_key_name: str
) -> None:
    """
    Creates a new secret with a customer-managed encryption key (CMEK).

        Args:
            project_id (str): ID of the Google Cloud project
            secret_id (str): ID of the secret to create
            kms_key_name (str): Full resource name of the KMS key
                (e.g., "projects/my-project/locations/global/keyRings/{keyringname}/cryptoKeys/{keyname}")

    Example:
            # Create a secret with a customer-managed encryption key
            create_secret_with_cmek(
                "my-project",
                "my-secret-with-cmek",
                "projects/my-project/locations/global/keyRings/my-keyring/cryptoKeys/my-key"
            )
    """
    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient()

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # Create the secret with automatic replication and CMEK.
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {
                    "automatic": {
                        "customer_managed_encryption": {
                            "kms_key_name": kms_key_name
                        }
                    }
                }
            },
        }
    )

    print(f"Created secret {secret.name} with CMEK key {kms_key_name}")


# [END secretmanager_create_secret_with_cmek]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument(
        "kms_key_name", help="full resource name of the KMS key"
    )
    args = parser.parse_args()

    create_secret_with_cmek(args.project_id, args.secret_id, args.kms_key_name)
