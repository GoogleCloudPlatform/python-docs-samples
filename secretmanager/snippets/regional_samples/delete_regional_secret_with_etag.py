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
Command line application and sample code for deleting an existing regional
secret.
"""

import argparse


# [START secretmanager_v1_delete_regional_secret_with_etag]
# Import the Secret Manager client library and types.
from google.cloud import secretmanager_v1


def delete_regional_secret_with_etag(
    project_id: str,
    location_id: str,
    secret_id: str,
    etag: str,
) -> None:
    """
    Deletes the regional secret with the given name, etag, and all of its versions.
    """

    # Endpoint to call the regional secret manager sever.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret.
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Build the request
    request = secretmanager_v1.types.service.DeleteSecretRequest(
        name=name,
        etag=etag,
    )

    # Delete the secret.
    client.delete_secret(request=request)


# [END secretmanager_v1_delete_regional_secret_with_etag]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument("secret_id", help="id of the secret to delete")
    parser.add_argument("etag", help="current etag of the secret to delete")
    args = parser.parse_args()

    delete_regional_secret_with_etag(
        args.project_id, args.location_id, args.secret_id, args.etag
    )
