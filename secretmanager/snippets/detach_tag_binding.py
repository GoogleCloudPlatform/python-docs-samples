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

import argparse

# [START secretmanager_detach_tag_binding]
from google.cloud import resourcemanager_v3


def detach_tag(project_id: str, secret_id: str, tag_value: str) -> None:
    """
    Detaches a tag value from a secret.

    Args:
        project_id (str): The project ID where the secret exists.
        secret_id (str): The ID of the secret from which to detach the tag.
        tag_value (str): The tag value to detach (e.g., "tagValues/123456789012").

    Example:
        # Detach a tag value from a secret
        detach_tag("my-project", "my-secret", "tagValues/123456789012")
    """
    # Create the Resource Manager client.
    client = resourcemanager_v3.TagBindingsClient()

    # Build the resource name of the parent secret.
    secret_name = f"projects/{project_id}/secrets/{secret_id}"
    parent = f"//secretmanager.googleapis.com/{secret_name}"

    # Find the binding name for the given tag value
    binding_name = None
    request = resourcemanager_v3.ListTagBindingsRequest(parent=parent)

    for binding in client.list_tag_bindings(request=request):
        if binding.tag_value == tag_value:
            binding_name = binding.name
            break

    if binding_name is None:
        print(f"Tag binding for value {tag_value} not found on {secret_name}.")
        return

    # Delete the tag binding
    request = resourcemanager_v3.DeleteTagBindingRequest(name=binding_name)
    operation = client.delete_tag_binding(request=request)

    # Wait for the operation to complete
    operation.result()

    print(f"Detached tag value {tag_value} from {secret_name}")


# [END secretmanager_detach_tag_binding]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to detach tag from")
    parser.add_argument(
        "tag_value",
        help="tag value to detach (e.g., 'tagValues/123456789012')",
    )
    args = parser.parse_args()

    detach_tag(args.project_id, args.secret_id, args.tag_value)
