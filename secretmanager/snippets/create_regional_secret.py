#!/usr/bin/env python

# Copyright 2019 Google LLC
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
command line application and sample code for creating a new regional secret.
"""

import argparse
from typing import Optional

from google.cloud import secretmanager_v1


# [START secretmanager_v1_create_regional_secret]
def create_regional_secret(
        project_id: str, location_id : str,  secret_id: str, ttl: Optional[str] = None
) -> secretmanager_v1.Secret:
    """
    Create a new regional secret with the given name. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.

     Args:
        project_id (str): The project ID where the secret is to be created.
        location_id(str): The location ID where the secret is to be created.
        secret_id (str): The ID to assign to the new secret. This ID must be unique within the project.
        ttl (Optional[str]): An optional string that specifies the secret's time-to-live in seconds with
                             format (e.g., "900s" for 15 minutes). If specified, the secret
                             versions will be automatically deleted upon reaching the end of the TTL period.

    Returns:
        secretmanager_v1.Secret: An object representing the newly created secret, containing details like the
                              secret's name, replication settings, and optionally its TTL.

    Example:
        # Create a secret with automatic replication and no TTL
        new_secret = create_secret("my-project", "location", "my-new-secret")

        # Create a secret with a TTL of 30 days
        new_secret_with_ttl = create_secret("my-project", "location", "my-timed-secret", "7776000s")
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager_v1


    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"
    
    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(client_options={
        "api_endpoint": api_endpoint
    })

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Create the secret.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"ttl": ttl},
        }
    )

    # Print the new secret name.
    print(f"Created secret: {response.name}")
    # [END secretmanager_v1_create_regional_secret]

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of the location where secret is to be created")
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument("ttl", help="time to live for secrets, f.e. '600s' ")
    args = parser.parse_args()

    create_secret(args.project_id, args.location_id, args.secret_id, args.ttl)
