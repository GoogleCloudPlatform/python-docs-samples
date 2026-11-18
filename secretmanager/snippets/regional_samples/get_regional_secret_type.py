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

"""
command line application and sample code for getting the secret type of a
regional secret.
"""

import argparse

# [START secretmanager_get_regional_secret_type]
# Import the Secret Manager client library.
from google.cloud import secretmanager_v1


def get_regional_secret_type(
    project_id: str, location_id: str, secret_id: str
) -> secretmanager_v1.Secret:
    """
    Gets the secret type of the given regional secret.

    Args:
        project_id (str): ID of the GCP project.
        location_id (str): Location of the regional secret, e.g. us-central1.
        secret_id (str): ID of the secret.

    Returns:
        secretmanager_v1.Secret: The secret, including its secret type.
    """

    # Endpoint to call the regional Secret Manager API.
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret.
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Get the secret.
    response = client.get_secret(request={"name": name})

    print(
        f"Found regional secret {response.name} with secret type "
        f"{response.secret_type.name}"
    )

    return response


# [END secretmanager_get_regional_secret_type]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of location where secret is stored")
    parser.add_argument("secret_id", help="id of the secret to get the type of")
    args = parser.parse_args()

    get_regional_secret_type(args.project_id, args.location_id, args.secret_id)
