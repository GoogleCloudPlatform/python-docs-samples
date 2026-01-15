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

# [START secretmanager_list_regional_secret_tag_bindings]
from google.api_core import client_options
from google.cloud import resourcemanager_v3


def list_regional_secret_tag_bindings(
    project_id: str, location_id: str, secret_id: str
) -> None:
    """
    Lists tag bindings for a regional secret.

    Args:
        project_id (str): ID of the Google Cloud project
        location_id (str): Region where the secret is stored (e.g., "us-central1")
        secret_id (str): The ID of the secret to list tag bindings for.

    Example:
        list_regional_secret_tag_bindings(
            "my-project",
            "us-central1",
            "my-regional-secret-with-cmek",
        )
    """
    # Set up the endpoint for the regional resource manager
    rm_endpoint = f"{location_id}-cloudresourcemanager.googleapis.com"
    client_option = client_options.ClientOptions(api_endpoint=rm_endpoint)

    # Create the Tag Bindings client with the regional endpoint
    tag_bindings_client = resourcemanager_v3.TagBindingsClient(
        client_options=client_option
    )

    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"

    # Format the parent resource for the tag bindings request
    parent = f"//secretmanager.googleapis.com/{name}"

    # List the tag bindings
    print(f"Tag bindings for {name}:")
    count = 0

    # Use the list_tag_bindings method to get all tag bindings
    request = resourcemanager_v3.ListTagBindingsRequest(parent=parent)
    tag_bindings = tag_bindings_client.list_tag_bindings(request=request)

    # Iterate through the results
    for binding in tag_bindings:
        print(f"- Tag Value: {binding.tag_value}")
        count += 1

    if count == 0:
        print(f"No tag bindings found for {name}.")


# [END secretmanager_list_regional_secret_tag_bindings]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument(
        "location_id", help="id of location where secret is stored"
    )
    parser.add_argument("secret_id", help="id of the secret in which to list")
    args = parser.parse_args()

    list_regional_secret_tag_bindings(
        args.project_id, args.location_id, args.secret_id
    )
