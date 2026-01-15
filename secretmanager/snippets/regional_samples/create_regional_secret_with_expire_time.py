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

# [START secretmanager_create_regional_secret_with_expire_time]
from datetime import datetime, timedelta, timezone

from google.api_core import client_options
from google.cloud import secretmanager
from google.protobuf import timestamp_pb2


def create_regional_secret_with_expire_time(
    project_id: str, secret_id: str, location_id: str
) -> None:
    """
    Creates a new regional secret with an expiration time.

    Args:
        project_id (str): ID of the Google Cloud project
        secret_id (str): ID of the secret to create
        location_id (str): Region where the secret should be stored (e.g., "us-central1")

    Example:
        # Create a regional secret that expires in 1 hour
        create_regional_secret_with_expire_time("my-project", "my-secret-with-expiry", "us-central1")
    """
    # Set expiration time to 1 hour from now
    expire_time = datetime.now(timezone.utc) + timedelta(hours=1)

    # Set up the endpoint for the specific region
    endpoint = f"secretmanager.{location_id}.rep.googleapis.com"
    client_option = client_options.ClientOptions(api_endpoint=endpoint)

    # Create the Secret Manager client with the regional endpoint
    client = secretmanager.SecretManagerServiceClient(
        client_options=client_option
    )

    # Build the resource name of the parent project with location
    parent = f"projects/{project_id}/locations/{location_id}"

    # Convert the Python datetime to a Protobuf Timestamp
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(expire_time)

    # Create the secret with expiration time
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"expire_time": timestamp},
        }
    )

    print(f"Created secret {secret.name} with expiration time {expire_time}")


# [END secretmanager_create_regional_secret_with_expire_time]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument(
        "location_id",
        help="region where the secret should be stored (e.g., us-central1)",
    )
    args = parser.parse_args()

    create_regional_secret_with_expire_time(
        args.project_id, args.secret_id, args.location_id
    )
