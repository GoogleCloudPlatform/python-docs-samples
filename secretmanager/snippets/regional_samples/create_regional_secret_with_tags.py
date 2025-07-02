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
command line application and sample code for creating a new secret with
tags.
"""

# [START secretmanager_create_regional_secret_with_tags]
import argparse

# Import the Secret Manager client library.
from google.cloud import secretmanager_v1


def create_regional_secret_with_tags(
    project_id: str,
    location_id: str,
    secret_id: str,
    tag_key: str,
    tag_value: str,
) -> secretmanager_v1.Secret:
    """
    Create a new regional secret with the given name and associated tags. A
    secret is a logical wrapper around a collection of secret versions. Secret
    versions hold the actual secret material.
    """

    # Endpoint to call the regional Secret Manager API.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the parent secret.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Create the secret.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "tags": {
                    tag_key: tag_value
                }
            },
        }
    )

    # Print the new secret name.
    print(f"Created secret: {response.name}")

    return response


# [END secretmanager_create_regional_secret_with_tags]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument(
        "location_id", help="id of the location where secret is to be created"
    )
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument("tag_key", help="key of the tag you want to add")
    parser.add_argument("tag_value", help="value of the tag you want to add")
    args = parser.parse_args()

    create_regional_secret_with_tags(
        args.project_id, args.location_id, args.secret_id, args.tag_key, args.tag_value
    )
