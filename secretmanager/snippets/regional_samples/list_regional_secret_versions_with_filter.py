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
Command line application and sample code for listing secret versions of a
regional secret.
"""

import argparse


# [START secretmanager_v1_list_regional_secret_versions_with_filter]
# Import the Secret Manager client library.
from google.cloud import secretmanager_v1


def list_regional_secret_versions_with_filter(
    project_id: str,
    location_id: str,
    secret_id: str,
    filter_str: str = "state:ENABLED",
) -> None:
    """
    Lists all secret versions in the given secret and their metadata.
    """

    # Endpoint to call the regional secret manager sever.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the parent secret.
    parent = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    secret_versions = client.list_secret_versions(
        request={"parent": parent, "filter": filter_str}
    )

    # List all secret versions.
    for version in secret_versions:
        print(f"Found secret version: {version.name}")


# [END secretmanager_v1_list_regional_secret_versions_with_filter]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument("secret_id", help="id of the secret from which to act")
    parser.add_argument("filter", help="filter string to apply")
    args = parser.parse_args()

    list_regional_secret_versions_with_filter(
        args.project_id, args.secret_id, args.filter
    )
