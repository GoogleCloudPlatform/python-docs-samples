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

# [START secretmanager_delete_secret_rotation]
from google.cloud import secretmanager
from google.protobuf.field_mask_pb2 import FieldMask


def delete_secret_rotation(project_id: str, secret_id: str) -> None:
    """
    Removes the rotation configuration from a secret.

    Args:
        project_id (str): ID of the Google Cloud project
        secret_id (str): ID of the secret with rotation to remove
    Example:
        # Remove the rotation configuration from a secret
        delete_secret_rotation(
            "my-project",
            "my-secret-with-rotation"
        )
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret
    name = client.secret_path(project_id, secret_id)

    # Create the update mask.
    update_mask = FieldMask(paths=["rotation"])

    # Build the request.
    request = {"secret": {"name": name}, "update_mask": update_mask}

    # Update the secret.
    secret = client.update_secret(request=request)

    print(f"Removed rotation from secret {secret.name}")


# [END secretmanager_delete_secret_rotation]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to act on")
    args = parser.parse_args()

    delete_secret_rotation(args.project_id, args.secret_id)
