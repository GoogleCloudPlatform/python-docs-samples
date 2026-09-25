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
command line application and sample code for getting the secret type of a
secret.
"""

# [START secretmanager_get_secret_type]
import argparse

# Import the Secret Manager client library.
from google.cloud import secretmanager


def get_secret_type(project_id: str, secret_id: str) -> secretmanager.Secret:
    """
    Get and print the secret type (e.g. CLOUD_SQL_DB_CREDENTIALS,
    ACCESS_KEY, CERTIFICATE, OTHER_DB_CREDENTIALS, OTHER, or
    SECRET_TYPE_UNSPECIFIED for a secret with no type restriction) of the
    given secret.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Get the secret.
    response = client.get_secret(request={"name": name})

    print(f"Found secret {response.name} with secret type {response.secret_type.name}")

    return response


# [END secretmanager_get_secret_type]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to get the type of")
    args = parser.parse_args()

    get_secret_type(args.project_id, args.secret_id)
