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
Command line application and sample code for adding a secret version to a
regional secret with the specified payload to an existing regional secret.
"""

import argparse

# [START secretmanager_v1_add_regional_secret_version]
from google.cloud import secretmanager_v1
import google_crc32c


def add_regional_secret_version(
    project_id: str,
    location_id: str,
    secret_id: str,
    payload: str,
) -> secretmanager_v1.SecretVersion:
    """
    Adds a new secret version to the given secret with the provided payload.
    """

    # Endpoint to call the regional secret manager sever.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the parent secret.
    parent = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload_bytes = payload.encode("UTF-8")

    # Calculate payload checksum. Passing a checksum in add-version request
    # is optional.
    crc32c = google_crc32c.Checksum()
    crc32c.update(payload_bytes)

    # Add the secret version.
    response = client.add_secret_version(
        request={
            "parent": parent,
            "payload": {
                "data": payload_bytes,
                "data_crc32c": int(crc32c.hexdigest(), 16),
            },
        }
    )

    # Print the new secret version name.
    print(f"Added secret version: {response.name}")
    return response


# [END secretmanager_v1_add_regional_secret_version]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument("secret_id", help="id of the secret in which to add")
    parser.add_argument("payload", help="secret material payload")
    args = parser.parse_args()

    add_regional_secret_version(
        args.project_id, args.location_id, args.secret_id, args.payload
    )
