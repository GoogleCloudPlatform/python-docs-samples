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

# [START secretmanager_delete_secret_expiration]
from google.cloud import secretmanager
from google.protobuf.field_mask_pb2 import FieldMask


def delete_secret_expiration(project_id: str, secret_id: str) -> None:
    """
    Removes the expiration time from a secret.

    Args:
        project_id (str): ID of the Google Cloud project
        secret_id (str): ID of the secret to update
    Example:
        # Remove the expiration time from a secret that was previously scheduled for deletion
        delete_secret_expiration(
            "my-project",
            "my-secret-with-expiration"
        )
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret
    name = client.secret_path(project_id, secret_id)

    # Create the update mask.
    update_mask = FieldMask(paths=["expire_time"])

    # Build the request.
    request = {"secret": {"name": name}, "update_mask": update_mask}

    # Update the secret.
    secret = client.update_secret(request=request)

    print(f"Removed expiration from secret {secret.name}")


# [END secretmanager_delete_secret_expiration]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to act on")
    args = parser.parse_args()

    delete_secret_expiration(args.project_id, args.secret_id)
