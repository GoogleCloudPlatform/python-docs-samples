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
command line application and sample code for listing annotations of a
secret.
"""
# [START secretmanager_view_secret_annotations]
import argparse

# Import the Secret Manager client library.
from google.cloud import secretmanager


def view_secret_annotations(project_id: str, secret_id: str) -> None:
    """
    List all secret annotations in the given secret.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    name = client.secret_path(project_id, secret_id)

    response = client.get_secret(request={"name": name})

    print(f"Got secret {response.name} with annotations :")
    for key in response.annotations:
        print(f"{key} : {response.annotations[key]}")


# [END secretmanager_view_secret_annotations]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret in which to list")
    args = parser.parse_args()

    view_secret_annotations(args.project_id, args.secret_id)
