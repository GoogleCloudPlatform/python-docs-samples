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
"""
command line application and sample code for creating a new secret then
bind the tag to that secret.
"""

# [START secretmanager_bind_tags_to_secret]
import argparse

# Import the Secret Manager and Resource Manager client library.
from google.cloud import resourcemanager_v3
from google.cloud import secretmanager


def bind_tags_to_secret(
    project_id: str,
    secret_id: str,
    tag_value: str,
) -> resourcemanager_v3.TagBinding:
    """
    Create a new secret with the given name, and then bind an existing tag to it.
    A secret is a logical wrapper around a collection of secret versions. Secret
    versions hold the actual secret material.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # Create the secret.
    secret_response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {"automatic": {}},
            },
        }
    )

    # Print the new secret name.
    print(f"Created secret: {secret_response.name}")

    # Create the resource manager client
    resource_manager_client = resourcemanager_v3.TagBindingsClient()

    # Create the tag binding
    request = resourcemanager_v3.CreateTagBindingRequest(
        tag_binding=resourcemanager_v3.TagBinding(
            parent=f"//secretmanager.googleapis.com/{secret_response.name}",
            tag_value=f"{tag_value}",
        ),
    )

    # Create the tag binding
    operation = resource_manager_client.create_tag_binding(request=request)

    # Wait for the operation to complete
    response = operation.result()

    # Print the tag binding
    print(f"Created tag binding: {response.name}")

    return response


# [END secretmanager_bind_tags_to_secret]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument("tag_value", help="value of the tag you want to add")
    args = parser.parse_args()

    bind_tags_to_secret(args.project_id, args.secret_id, args.tag_value)
