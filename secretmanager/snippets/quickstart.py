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
command line application and sample code for creating an accessing a secret.
"""


def quickstart(_project_id: str, _secret_id: str) -> None:
    # [START secretmanager_quickstart]
    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # GCP project in which to store secrets in Secret Manager.
    project_id = "YOUR_PROJECT_ID"

    # ID of the secret to create.
    secret_id = "YOUR_SECRET_ID"

    # [END secretmanager_quickstart]
    project_id = _project_id
    secret_id = _secret_id
    # [START secretmanager_quickstart]
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the parent name from the project.
    parent = f"projects/{project_id}"

    # Create the parent secret.
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
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
    # [END secretmanager_quickstart]


if __name__ == "__main__":
    quickstart("YOUR_PROJECT_ID", "YOUR_SECRET_ID")
