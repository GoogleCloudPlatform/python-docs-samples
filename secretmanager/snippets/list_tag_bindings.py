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
command line application and sample code for listing tag bindings attached to a secret.
"""

import argparse

# [START secretmanager_list_tag_bindings]
# Import the Resource Manager client library.
from google.cloud import resourcemanager_v3
from google.cloud import secretmanager


def list_tag_bindings(project_id: str, secret_id: str) -> None:
    """
    Lists all tag bindings attached to a secret.

    Args:
        project_id (str): The project ID where the secret exists.
        secret_id (str): The ID of the secret to list tag bindings for.

    Example:
        # List tag bindings for a secret
        list_tag_bindings("my-project", "my-secret")
    """

    # Create the Resource Manager client.
    client = resourcemanager_v3.TagBindingsClient()
    sm_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    secret_name = sm_client.secret_path(project_id, secret_id)

    parent = f"//secretmanager.googleapis.com/{secret_name}"

    # List all tag bindings.
    tag_bindings = []
    request = resourcemanager_v3.ListTagBindingsRequest(parent=parent)

    # Retrieve and process tag bindings
    bindings = client.list_tag_bindings(request=request)
    count = 0

    print(f"Tag bindings for {secret_name}:")
    for binding in bindings:
        print(f"- Tag Value: {binding.tag_value}")
        tag_bindings.append(binding)
        count += 1

    if count == 0:
        print(f"No tag bindings found for {secret_name}.")


# [END secretmanager_list_tag_bindings]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument(
        "secret_id", help="id of the secret to list tag bindings for"
    )
    args = parser.parse_args()

    list_tag_bindings(args.project_id, args.secret_id)
