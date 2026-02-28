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

# [START secretmanager_update_secret_rotation]
from google.cloud import secretmanager_v1
from google.protobuf import duration_pb2
from google.protobuf.field_mask_pb2 import FieldMask


def update_secret_rotation(project_id: str, secret_id: str) -> None:
    """
    Updates the rotation period of a secret.

    Args:
        project_id (str): ID of the Google Cloud project
        secret_id (str): ID of the secret to update
    Example:
        # Update the rotation period of a secret to 60 days
        update_secret_rotation(
            "my-project",
            "my-secret-with-rotation",
        )
    """
    new_rotation_period_hours = 48
    # Create the Secret Manager client
    client = secretmanager_v1.SecretManagerServiceClient()

    # Build the resource name of the secret
    name = client.secret_path(project_id, secret_id)

    # Convert rotation period to protobuf Duration
    rotation_period = duration_pb2.Duration()
    rotation_period.seconds = (
        new_rotation_period_hours * 3600
    )  # Convert hours to seconds

    # Create the update mask
    update_mask = FieldMask(paths=["rotation.rotation_period"])

    # Build the request
    request = {
        "secret": {
            "name": name,
            "rotation": {"rotation_period": rotation_period},
        },
        "update_mask": update_mask,
    }

    # Update the secret
    result = client.update_secret(request=request)

    rotation_hours = result.rotation.rotation_period.seconds / 3600
    print(f"Updated secret {result.name} rotation period to {rotation_hours} hours")


# [END secretmanager_update_secret_rotation]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="ID of the GCP project")
    parser.add_argument("secret_id", help="ID of the secret to update")
    args = parser.parse_args()

    update_secret_rotation(
        args.project_id,
        args.secret_id,
    )
