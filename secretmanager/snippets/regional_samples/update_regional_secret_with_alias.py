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


# [START secretmanager_update_regional_secret_with_alias]
from google.api_core import client_options
from google.cloud import secretmanager_v1
from google.protobuf import field_mask_pb2


def update_regional_secret_with_alias(
    project_id: str, secret_id: str, location_id: str
) -> None:
    """
    Updates the alias map on an existing regional secret.

    Args:
        project_id (str): ID of the Google Cloud project
        secret_id (str): ID of the secret
        location_id (str): Region where the secret is stored (e.g., "us-central1")

    Example:
        # Update a regional secret with an alias
        update_regional_secret_with_alias(
            "my-project",
            "my-secret",
            "us-central1"
        )
    """
    # Construct the secret name from the component parts
    secret_name = (
        f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"
    )

    # Set up the endpoint for the specific region
    endpoint = f"secretmanager.{location_id}.rep.googleapis.com"
    client_option = client_options.ClientOptions(api_endpoint=endpoint)

    # Create the Secret Manager client with the regional endpoint
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options=client_option
    )

    # Create a field mask to update only the version_aliases field
    update_mask = field_mask_pb2.FieldMask(paths=["version_aliases"])

    # Update the secret with the new alias map
    result = client.update_secret(
        request={
            "secret": {"name": secret_name, "version_aliases": {"test": 1}},
            "update_mask": update_mask,
        }
    )

    print(f"Updated regional secret: {result.name}")


# [END secretmanager_update_regional_secret_with_alias]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret")
    parser.add_argument(
        "location_id",
        help="region where the secret is stored (e.g., us-central1)",
    )
    args = parser.parse_args()

    update_regional_secret_with_alias(
        args.project_id, args.secret_id, args.location_id
    )
