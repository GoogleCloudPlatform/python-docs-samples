#!/usr/bin/env python

# Copyright 2022 Google LLC
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
command line application and sample code for creating a new secret with
user managed replication.
"""

import argparse
import typing

from google.cloud import secretmanager


def create_ummr_secret(
    project_id: str,
    secret_id: str,
    locations: typing.List[str],
    ttl: typing.Optional[str] = None,
) -> secretmanager.Secret:
    """
    Create a new secret with the given name. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.

    Args:
        project_id (str): The project ID where the secret is to be created.
        secret_id (str): The unique identifier for the new secret within the project.
        locations (List[str]): A list of Google Cloud locations where the secret should be replicated.
        ttl (Optional[str]): An optional string that specifies the secret's time-to-live in seconds with
                             format (e.g., "900s" for 15 minutes). If specified, the secret versions will be
                             automatically deleted upon reaching the end of the TTL period.

    Returns:
        secretmanager.Secret: An object representing the newly created secret. This object includes information like the
                              secret's name and its replication configuration. If TTL is provided, it also configures how long
                              secret versions remain before being automatically deleted.

    Example:
        # Create a secret with user-managed replication across two locations without TTL
        new_secret = create_ummr_secret("my-project", "my-new-secret", ["us-east1", "europe-west1"])

        # Create a secret with a TTL of 30 days and user-managed replication across three locations
        new_secret_with_ttl = create_ummr_secret("my-project", "my-timed-secret", ["us-east1", "us-west1"], "7776000s")

    Note:
        This function requires that the `secretmanager` API is enabled on the cloud project and that the caller has the
        necessary permissions to create secrets. Ensure that `secretmanager.SecretManagerServiceClient` and the `secretmanager`
        library are correctly configured and authenticated. The specified locations must be valid Google Cloud locations.
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # Create the secret.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {
                    "user_managed": {"replicas": [{"location": x} for x in locations]}
                },
                "ttl": ttl,
            },
        }
    )

    # Print the new secret name.
    print(f"Created secret: {response.name}")

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument(
        "--locations", nargs="+", help="list of locations for secret replication"
    )
    args = parser.parse_args()

    create_ummr_secret(args.project_id, args.secret_id, args.locations)
