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
Command line application and sample code for getting metadata about a regional
secret version, but not the secret payload.
"""

import argparse


# [START secretmanager_v1_get_regional_secret_version]
# Import the Secret Manager client library.
from google.cloud import secretmanager_v1


def get_regional_secret_version(
    project_id: str,
    location_id: str,
    secret_id: str,
    version_id: str,
) -> secretmanager_v1.GetSecretVersionRequest:
    """
    Gets information about the given secret version. It does not include the
    payload data.
    """

    # Endpoint to call the regional secret manager sever.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}/versions/{version_id}"

    # Get the secret version.
    response = client.get_secret_version(request={"name": name})

    # Print information about the secret version.
    state = response.state.name
    print(f"Got secret version {response.name} with state {state}")

    return response


# [END secretmanager_v1_get_regional_secret_version]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument("secret_id", help="id of the secret from which to act")
    parser.add_argument("version_id", help="id of the version of secret to get")
    args = parser.parse_args()

    get_regional_secret_version(
        args.project_id, args.location_id, args.secret_id, args.version_id
    )
