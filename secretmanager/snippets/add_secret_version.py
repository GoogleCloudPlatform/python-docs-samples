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
command line application and sample code for adding a secret version with the
specified payload to an existing secret.
"""

import argparse

from google.cloud import secretmanager
import google_crc32c  # type: ignore


# [START secretmanager_add_secret_version]
def add_secret_version(
    project_id: str, secret_id: str, payload: str
) -> secretmanager.SecretVersion:
    """
    Add a new secret version to the given secret with the provided payload.
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    parent = client.secret_path(project_id, secret_id)

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
    # [END secretmanager_add_secret_version]
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret in which to add")
    parser.add_argument("payload", help="secret material payload")
    args = parser.parse_args()

    add_secret_version(args.project_id, args.secret_id, args.payload)
