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

# [START spanner_queue_receive_messages]
from datetime import datetime, timezone
import sys

from google.api_core import exceptions
from google.cloud import spanner


def receive_and_ack_queue_messages(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Streams messages from RECEIVE_UserTasks, checks leases, and acknowledges.

    Queue RECEIVE TVF queries require a strong read snapshot and return leased
    messages up to max_duration.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the UserTasks queue.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    queue_name = "UserTasks"
    sql = """
        SELECT UserId,
               MessageId,
               Payload,
               SpannerLeaseExpirationTimestamp
        FROM RECEIVE_UserTasks(max_duration => '2s', max_batch_size => 10)
    """
    acked_count = 0

    def ack_valid_messages(keys: list[list[int | str]]) -> None:
        with database.batch() as batch:
            for key in keys:
                batch.ack(queue=queue_name, key=key, ignore_not_found=True)

    try:
        with database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(sql))

        now = datetime.now(timezone.utc)
        valid_keys: list[list[int | str]] = [
            [int(user_id), str(msg_id)]
            for user_id, msg_id, _payload, lease_exp in rows
            if lease_exp is not None and lease_exp > now
        ]
        if valid_keys:
            ack_valid_messages(valid_keys)
            acked_count = len(valid_keys)
    except exceptions.NotFound as err:
        print(
            f"error: queue '{queue_name}' on database '{database_id}' "
            f"in instance '{instance_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to receive or ack messages from queue "
            f"'{queue_name}' on database '{database_id}' in instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Acknowledged Messages: {acked_count}")
        print(f"Queue Name: {queue_name}")
        print(f"Received Messages: {len(rows)}")


# [END spanner_queue_receive_messages]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Receive and acknowledge messages from a Cloud Spanner queue."
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

    receive_and_ack_queue_messages(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
