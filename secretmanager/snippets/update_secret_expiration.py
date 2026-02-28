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

# [START secretmanager_update_secret_expiration]
from datetime import datetime, timedelta
from google.protobuf import timestamp_pb2
from google.cloud import secretmanager


def update_secret_expiration(project_id: str, secret_id: str) -> None:
    """
    Update the expiration time of an existing secret.

    Args:
        project_id: ID of the Google Cloud project.
        secret_id: ID of the secret to update.

    Example:
        # Update the expiration time of a secret to 48 hours from now
        update_secret_expiration(
            "my-project",
            "my-secret-with-expiration"
        )
    """
    new_expire_time = datetime.now() + timedelta(hours=2)

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Update the expire_time.
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(new_expire_time)
    secret = {"name": name, "expire_time": timestamp}
    update_mask = {"paths": ["expire_time"]}
    response = client.update_secret(
        request={"secret": secret, "update_mask": update_mask}
    )

    # Print the updated secret name.
    print(
        f"Updated secret {response.name} expiration time to {new_expire_time}"
    )


# [END secretmanager_update_secret_expiration]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="ID of the GCP project")
    parser.add_argument("secret_id", help="ID of the secret to update")
    args = parser.parse_args()

    update_secret_expiration(args.project_id, args.secret_id)
