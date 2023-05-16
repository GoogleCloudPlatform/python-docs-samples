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

import argparse


# [START secretmanager_update_secret]
def update_secret(project_id: str, secret_id: str):
    """
    Update the metadata about an existing secret.
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Update the secret.
    secret = {"name": name, "labels": {"secretmanager": "rocks"}}
    update_mask = {"paths": ["labels"]}
    response = client.update_secret(
        request={"secret": secret, "update_mask": update_mask}
    )

    # Print the new secret name.
    print(f"Updated secret: {response.name}")
    # [END secretmanager_update_secret]

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("--secret-id", required=True)
    args = parser.parse_args()

    update_secret(args.project_id, args.secret_id)
