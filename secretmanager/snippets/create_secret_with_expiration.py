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

# [START secretmanager_create_secret_with_expiration]
from datetime import datetime, timedelta, timezone

from google.cloud import secretmanager
from google.protobuf import timestamp_pb2


def create_secret_with_expiration(project_id: str, secret_id: str) -> None:
    """
    Create a new secret with an expiration time.

    Args:
        project_id (str): The ID of the project where the secret will be created.
        secret_id (str): The ID for the secret to create.

    Example:
        # Create a secret that expires in 1 hour
        create_secret_with_expiration("my-project", "my-secret-with-expiry")
    """
    expire_time = datetime.now(timezone.utc) + timedelta(hours=1)
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # Convert the Python datetime to a Protobuf Timestamp
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(expire_time)

    # Create the secret with automatic replication and expiration time.
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {
                    "automatic": {},
                },
                "expire_time": timestamp,
            },
        }
    )

    print(f"Created secret {secret.name} with expiration time {expire_time}")


# [END secretmanager_create_secret_with_expiration]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    args = parser.parse_args()

    create_secret_with_expiration(args.project_id, args.secret_id)
