#!/usr/bin/env python

# Copyright 2025 Google LLC
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

# [START secretmanager_disable_secret_delayed_destroy]

# Import the Secret Manager client library.
from google.cloud import secretmanager


def disable_secret_with_delayed_destroy(
    project_id: str, secret_id: str
) -> secretmanager.Secret:
    """
    Disable the version destroy ttl on the given secret version.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Delayed destroy of the secret version.
    secret = {"name": name}
    update_mask = {"paths": ["version_destroy_ttl"]}
    response = client.update_secret(request={"secret": secret, "update_mask": update_mask})

    # Print the new secret name.
    print(f"Disabled delayed destroy on secret: {response.name}")

    return response

# [END secretmanager_disable_secret_delayed_destroy]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret from which to act")
    args = parser.parse_args()

    disable_secret_with_delayed_destroy(
        args.project_id, args.secret_id
    )
