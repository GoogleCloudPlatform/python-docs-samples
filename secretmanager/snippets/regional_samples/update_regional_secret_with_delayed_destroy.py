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

import argparse

# [START secretmanager_update_regional_secret_with_delayed_destroy]

# Import the Secret Manager client library.
from google.cloud import secretmanager_v1
from google.protobuf.duration_pb2 import Duration


def update_regional_secret_with_delayed_destroy(
    project_id: str, location_id: str, secret_id: str, new_version_destroy_ttl: int
) -> secretmanager_v1.Secret:
    """
    Update the version destroy ttl on an existing secret.

    Args:
      project_id: Parent project id
      location_id: Location of the secret
      secret_id: ID of the secret or fully qualified identifier for the secret
      new_version_destroy_ttl: Secret Version TTL value in seconds

    Returns:
      Regional secret with updated version destroy ttl value
    """

    # Endpoint to call the regional secret manager sever
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name.
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Get the secret.
    response = client.get_secret(request={"name": name})

    # Update the secret.
    secret = {"name": name, "version_destroy_ttl": Duration(seconds=new_version_destroy_ttl)}
    update_mask = {"paths": ["version_destroy_ttl"]}
    response = client.update_secret(
        request={"secret": secret, "update_mask": update_mask}
    )

    # Print the new secret name.
    print(f"Updated secret: {response.name}")

    return response

# [END secretmanager_update_regional_secret_with_delayed_destroy]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument(
        "location_id", help="id of the location where secret is to be created"
    )
    parser.add_argument("secret_id", help="id of the secret to act on")
    parser.add_argument(
        "new_version_destroy_ttl", help="version_destroy_ttl you want to add (in seconds)"
    )
    args = parser.parse_args()

    update_regional_secret_with_delayed_destroy(
        args.project_id, args.location_id, args.secret_id, int(args.new_version_destroy_ttl)
    )
