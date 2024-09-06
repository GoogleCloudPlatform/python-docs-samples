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
Command line application and sample code for creating an accessing a secret.
"""


def regional_quickstart(project_id: str, location_id: str, secret_id: str) -> None:
    # [START secretmanager_regional_quickstart]
    # Import the Secret Manager client library.
    from google.cloud import secretmanager_v1

    # TODO (developer): uncomment variables and assign a value.

    # GCP project in which to store secrets in Secret Manager.
    # project_id = "YOUR_PROJECT_ID"

    # Location where the secret is to be stored
    # location_id = "YOUR_LOCATION_ID"

    # ID of the secret to create.
    # secret_id = "YOUR_SECRET_ID"

    # Endpoint to call the regional secret manager sever
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client.
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the parent name from the project.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Create the parent secret.
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
        }
    )

    # Add the secret version.
    version = client.add_secret_version(
        request={"parent": secret.name, "payload": {"data": b"hello world!"}}
    )

    # Access the secret version.
    response = client.access_secret_version(request={"name": version.name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    print(f"Plaintext: {payload}")
    # [END secretmanager_regional_quickstart]


if __name__ == "__main__":
    regional_quickstart("YOUR_PROJECT_ID", "YOUR_LOCATION_ID", "YOUR_SECRET_ID")
