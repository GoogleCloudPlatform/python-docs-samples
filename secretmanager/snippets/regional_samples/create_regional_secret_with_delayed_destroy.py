#!/usr/bin/env python

# Copyright 2025 Google LLC
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
Command line application and sample code for creating a new secret with
delayed destroy.
"""

import argparse

# [START secretmanager_create_regional_secret_with_delayed_destroy]

# Import the Secret Manager client library.
from google.cloud import secretmanager_v1
from google.protobuf.duration_pb2 import Duration


def create_regional_secret_with_delayed_destroy(
    project_id: str,
    location_id: str,
    secret_id: str,
    version_destroy_ttl: int,
) -> secretmanager_v1.Secret:
    """
    Create a new secret with the given name and version_destroy_ttl. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.

    Args:
      project_id: Parent project id
      location_id: Location of the secret
      secret_id: ID of the secret or fully qualified identifier for the secret
      version_destroy_ttl: Secret Version TTL after destruction request

    Returns:
      Regional secret with delayed destroy
      """

    # Endpoint to call the regional secret manager sever
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Create the secret.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"version_destroy_ttl": Duration(seconds=version_destroy_ttl)},
        }
    )

    # Print the new secret name.
    print(f"Created secret: {response.name}")

    return response

# [END secretmanager_create_regional_secret_with_delayed_destroy]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument(
        "location_id", help="id of the location where secret is to be created"
    )
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument(
        "version_destroy_ttl", help="version_destroy_ttl you want to add (in seconds)"
    )
    args = parser.parse_args()

    create_regional_secret_with_delayed_destroy(
        args.project_id, args.location_id, args.secret_id, int(args.version_destroy_ttl)
    )
