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

# [START spanner_get_commit_stats]
import logging
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def get_commit_stats(project_id: str, instance_id: str, database_id: str) -> None:
    """Requests and prints Spanner CommitStats for a read-write transaction.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Singers.
    """
    client = spanner.Client(project=project_id)
    stats_logger = logging.Logger("spanner_commit_stats")
    stats_logger.addHandler(logging.NullHandler())
    database = client.instance(instance_id).database(database_id, logger=stats_logger)
    database.log_commit_stats = True
    committed_txn: spanner_v1.transaction.Transaction | None = None
    inserted_rows = 0

    def insert_singers(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal committed_txn, inserted_rows
        committed_txn = transaction
        inserted_rows = transaction.execute_update("""
            INSERT INTO Singers (SingerId, FirstName, LastName)
            VALUES (110, 'Virginia', 'Watson')
        """)

    try:
        database.run_in_transaction(insert_singers)
    except exceptions.AlreadyExists as err:
        print(
            f"error: singer row already exists on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: commit-stats transaction failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        mutation_count = (
            committed_txn.commit_stats.mutation_count
            if committed_txn and committed_txn.commit_stats
            else 0
        )
        print(f"Resource ID: {database_id}")
        print(f"Inserted Rows: {inserted_rows}")
        print(f"Mutation Count: {mutation_count}")


# [END spanner_get_commit_stats]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Collect Spanner CommitStats mutation_count from a transaction."
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

    get_commit_stats(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
