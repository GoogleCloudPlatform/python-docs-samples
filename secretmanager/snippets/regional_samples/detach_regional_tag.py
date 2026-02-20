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

# [START secretmanager_detach_regional_tag_binding]
from google.cloud import resourcemanager_v3
from google.api_core import client_options


def detach_regional_tag(
    project_id: str, location_id: str, secret_id: str, tag_value: str
) -> None:
    """
    Detaches a tag value from a regional secret.

    Args:
        project_id (str): ID of the Google Cloud project
        location_id (str): Region where the secret is stored (e.g., "us-central1")
        secret_id (str): ID of the secret
        tag_value (str): Tag value to detach (e.g., "tagValues/123456789012")

    Example:
        # Detach a tag value from a regional secret
        detach_regional_tag(
            "my-project",
            "us-central1",
            "my-secret",
            "tagValues/123456789012"
        )
    """
    # Set up the endpoint for the regional resource manager
    rm_endpoint = f"{location_id}-cloudresourcemanager.googleapis.com"
    client_option = client_options.ClientOptions(api_endpoint=rm_endpoint)

    # Create the Tag Bindings client with the regional endpoint
    tag_bindings_client = resourcemanager_v3.TagBindingsClient(
        client_options=client_option
    )

    secret_name = (
        f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}"
    )

    # Format the parent resource for the tag bindings request
    parent = f"//secretmanager.googleapis.com/{secret_name}"

    # Find the binding with the specified tag value
    binding_name = None
    request = resourcemanager_v3.ListTagBindingsRequest(parent=parent)
    tag_bindings = tag_bindings_client.list_tag_bindings(request=request)

    for binding in tag_bindings:
        if binding.tag_value == tag_value:
            binding_name = binding.name
            break

    if binding_name is None:
        print(f"Tag binding for value {tag_value} not found on {secret_name}.")
        return

    # Delete the tag binding
    request = resourcemanager_v3.DeleteTagBindingRequest(name=binding_name)
    operation = tag_bindings_client.delete_tag_binding(request=request)

    # Wait for the operation to complete
    operation.result()

    print(f"Detached tag value {tag_value} from {secret_name}")


# [END secretmanager_detach_regional_tag_binding]


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
    parser.add_argument("secret_id", help="id of the secret")
    parser.add_argument(
        "tag_value", help="tag value to detach (e.g., tagValues/123456789012)"
    )
    args = parser.parse_args()

    detach_regional_tag(
        args.project_id, args.location_id, args.secret_id, args.tag_value
    )
