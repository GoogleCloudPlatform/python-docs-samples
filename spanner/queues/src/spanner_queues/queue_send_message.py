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

# [START spanner_queue_send_message]
import base64
from datetime import datetime, timezone
import sys
import uuid

from google.api_core import exceptions
from google.cloud import spanner


def send_queue_message(project_id: str, instance_id: str, database_id: str) -> None:
    """Sends a message to a Cloud Spanner queue using a Send mutation.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Users and UserTasks.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    queue_name = "UserTasks"
    user_id = 1
    message_id = str(uuid.uuid4())
    # Python protobuf Value encodes BYTES payloads from base64-encoded strings.
    encoded_payload = base64.b64encode(b"example-task-payload").decode("ascii")
    deliver_time = datetime.now(timezone.utc)

    try:
        with database.batch() as batch:
            batch.send(
                queue=queue_name,
                key=[user_id, message_id],
                payload=encoded_payload,
                deliver_time=deliver_time,
            )
    except exceptions.NotFound as err:
        print(
            f"error: queue '{queue_name}' or parent row on database "
            f"'{database_id}' in instance '{instance_id}'"
            f" was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to send message to queue '{queue_name}' on "
            f"database '{database_id}' in instance '{instance_id}'"
            f": {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Message ID: {message_id}")
        print(f"Queue Name: {queue_name}")
        print(f"User ID: {user_id}")


# [END spanner_queue_send_message]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Send a message to a Cloud Spanner queue."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
        help="Spanner instance ID (default: $SPANNER_INSTANCE_ID)",
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
        help="Spanner database ID (default: $SPANNER_DATABASE_ID)",
    )
    args = parser.parse_args()

    send_queue_message(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
