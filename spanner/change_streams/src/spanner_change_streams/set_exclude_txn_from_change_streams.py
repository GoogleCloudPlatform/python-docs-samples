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

# [START spanner_set_exclude_txn_from_change_streams]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def set_exclude_txn_from_change_streams(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Runs a read-write transaction excluded from change stream capture.

    Only change streams created or altered with `allow_txn_exclusion = true`
    honor transaction-level exclusion.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Singers and a change
            stream with allow_txn_exclusion = true.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    modified_statements = 0

    def insert_and_update_singer(transaction: spanner_v1.Transaction) -> None:
        nonlocal modified_statements
        inserted = transaction.execute_update("""
            INSERT OR UPDATE Singers (SingerId, FirstName, LastName)
            VALUES (101, ' Virginia', 'Watson')
        """)
        updated = transaction.execute_update(
            "UPDATE Singers SET FirstName = 'Virginia' WHERE SingerId = 101"
        )
        modified_statements = int(inserted) + int(updated)

    try:
        database.run_in_transaction(
            insert_and_update_singer,
            exclude_txn_from_change_streams=True,
        )
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: change-stream excluded transaction failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Modified Statements: {modified_statements}")


# [END spanner_set_exclude_txn_from_change_streams]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Exclude a read-write Spanner transaction from change streams."
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

    set_exclude_txn_from_change_streams(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
