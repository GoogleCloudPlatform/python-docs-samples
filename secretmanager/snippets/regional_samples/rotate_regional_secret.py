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
command line application and sample code for triggering a managed
rotation of a Cloud SQL DB credentials secret.
"""

# [START secretmanager_rotate_regional_secret]
import argparse

# Import the Secret Manager client library.
from google.cloud import secretmanager_v1


def rotate_regional_secret(
    project_id: str,
    location_id: str,
    secret_id: str,
) -> secretmanager_v1.SecretVersion:
    """
    Trigger a managed rotation for a Cloud SQL DB credentials secret.
    Managed rotation must already be enabled on the secret (see
    enable_regional_secret_managed_rotation.py). Each call generates a new
    password, updates the Cloud SQL user, and adds the result as a new
    secret version.
    """

    # Endpoint to call the regional Secret Manager API.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret.
    parent = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Rotate the secret.
    response = client.rotate_secret(request={"parent": parent})

    print(f"Rotated secret, created secret version: {response.name}")

    return response


# [END secretmanager_rotate_regional_secret]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument(
        "secret_id", help="id of the Cloud SQL DB credentials secret to rotate"
    )
    args = parser.parse_args()

    rotate_regional_secret(args.project_id, args.location_id, args.secret_id)
