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

# [START secretmanager_create_regional_secret_with_rotation]
from datetime import datetime, timedelta, timezone

from google.api_core import client_options
from google.cloud import secretmanager_v1
from google.protobuf import duration_pb2, timestamp_pb2


def create_regional_secret_with_rotation(
    project_id: str, secret_id: str, location_id: str, topic_name: str
) -> None:
    """
    Creates a new regional secret with rotation configured.

    Args:
        project_id (str): ID of the Google Cloud project
        secret_id (str): ID of the secret to create
        location_id (str): Region where the secret should be stored (e.g., "us-central1")
        topic_name (str): Full resource name of the Pub/Sub topic for notifications
            (e.g., "projects/my-project/topics/my-topic")

    Example:
        # Create a regional secret with rotation
        create_regional_secret_with_rotation(
            "my-project",
            "my-secret-with-rotation",
            "us-central1",
            "projects/my-project/topics/my-topic"
        )
    """
    # Set rotation period to 24 hours
    rotation_period = timedelta(hours=24)

    # Set next rotation time to 24 hours from now
    next_rotation_time = datetime.now(timezone.utc) + timedelta(hours=24)

    # Set up the endpoint for the specific region
    endpoint = f"secretmanager.{location_id}.rep.googleapis.com"
    client_option = client_options.ClientOptions(api_endpoint=endpoint)

    # Create the Secret Manager client with the regional endpoint
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options=client_option
    )

    # Build the resource name of the parent project with location
    parent = f"projects/{project_id}/locations/{location_id}"

    # Convert the Python datetime to a Protobuf Timestamp
    next_rotation_timestamp = timestamp_pb2.Timestamp()
    next_rotation_timestamp.FromDatetime(next_rotation_time)

    # Convert the Python timedelta to a Protobuf Duration
    rotation_period_proto = duration_pb2.Duration()
    rotation_period_proto.FromTimedelta(rotation_period)

    # Create the secret with rotation configuration and topic
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "topics": [{"name": topic_name}],
                "rotation": {
                    "next_rotation_time": next_rotation_timestamp,
                    "rotation_period": rotation_period_proto,
                },
            },
        }
    )

    print(
        f"Created secret {secret.name} with rotation period {rotation_period} and topic {topic_name}"
    )


# [END secretmanager_create_regional_secret_with_rotation]


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
    parser.add_argument(
        "topic_name",
        help="full resource name of the Pub/Sub topic for notifications",
    )
    args = parser.parse_args()

    create_regional_secret_with_rotation(
        args.project_id, args.secret_id, args.location_id, args.topic_name
    )
