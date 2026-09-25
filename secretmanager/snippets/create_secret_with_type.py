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
"""
command line application and sample code for creating a new secret with a
secret type restriction.
"""

# [START secretmanager_create_secret_with_type]
import argparse

# Import the Secret Manager client library.
from google.cloud import secretmanager


def create_secret_with_type(
    project_id: str,
    secret_id: str,
    secret_type: secretmanager.Secret.SecretType,
) -> secretmanager.Secret:
    """
    Create a new secret with the given secret type restriction (e.g.
    ACCESS_KEY, CERTIFICATE, OTHER_DB_CREDENTIALS, or OTHER -- use
    CLOUD_SQL_DB_CREDENTIALS only for a regional secret that will go
    through enable_regional_secret_managed_rotation; see the
    regional_samples directory). Unlike CLOUD_SQL_DB_CREDENTIALS, these
    other secret types are plain metadata tags: they don't require any
    additional credentials payload at creation time.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # Create the secret, with the given secret type restriction.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {"automatic": {}},
                "secret_type": secret_type,
            },
        }
    )

    # Print the new secret name.
    print(f"Created secret with secret type: {response.name}")

    return response


# [END secretmanager_create_secret_with_type]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument(
        "secret_type",
        choices=[t.name for t in secretmanager.Secret.SecretType if t.value != 0],
        help="secret type restriction to apply",
    )
    args = parser.parse_args()

    create_secret_with_type(
        args.project_id,
        args.secret_id,
        secretmanager.Secret.SecretType[args.secret_type],
    )
