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

# [START secretmanager_create_secret_with_topic]
from google.cloud import secretmanager


def create_secret_with_topic(
    project_id: str, secret_id: str, topic_name: str
) -> None:
    """
    Creates a new secret with a notification topic configured.

    Args:
        project_id (str): ID of the Google Cloud project
        secret_id (str): ID of the secret to create
        topic_name (str): Full name of the topic in the format "projects/my-project/topics/my-topic"
    Example:
        # Create a secret with a Pub/Sub notification configuration
        create_secret_with_topic(
            "my-project",
            "my-secret-with-notifications",
            "projects/my-project/topics/my-secret-topic"
        )
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the parent name.
    parent = f"projects/{project_id}"

    # Create the secret with topic configuration.
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                "replication": {"automatic": {}},
                "topics": [{"name": topic_name}],
            },
        }
    )

    print(f"Created secret {secret.name} with topic {topic_name}")


# [END secretmanager_create_secret_with_topic]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    parser.add_argument(
        "topic_name",
        help="name of the topic in the format 'projects/my-project/topics/my-topic'",
    )
    args = parser.parse_args()

    create_secret_with_topic(args.project_id, args.secret_id, args.topic_name)
