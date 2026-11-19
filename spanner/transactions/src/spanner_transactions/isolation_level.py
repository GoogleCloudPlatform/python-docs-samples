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

# [START spanner_isolation_level]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def run_transaction_with_isolation_level(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Configures client-default and per-transaction isolation levels.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Albums.
    """
    default_options = spanner_v1.DefaultTransactionOptions(
        isolation_level=spanner_v1.TransactionOptions.IsolationLevel.SERIALIZABLE  # type: ignore[arg-type]
    )
    client = spanner.Client(
        project=project_id, default_transaction_options=default_options
    )
    database = client.instance(instance_id).database(database_id)
    txn_isolation = spanner_v1.TransactionOptions.IsolationLevel.REPEATABLE_READ
    previous_title = ""
    updated_rows = 0

    def update_albums_with_isolation(
        transaction: spanner_v1.transaction.Transaction,
    ) -> None:
        nonlocal previous_title, updated_rows
        row = next(
            iter(
                transaction.execute_sql(
                    "SELECT AlbumTitle FROM Albums WHERE SingerId = 1 AND AlbumId = 1"
                )
            ),
            None,
        )
        if row is None:
            raise ValueError("Album row not found.")
        previous_title = str(row[0])
        updated_rows = transaction.execute_update("""
            UPDATE Albums SET AlbumTitle = 'A New Title'
            WHERE SingerId = 1 AND AlbumId = 1
        """)

    try:
        database.run_in_transaction(
            update_albums_with_isolation, isolation_level=txn_isolation
        )
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except (exceptions.GoogleAPICallError, ValueError) as err:
        message = getattr(err, "message", str(err))
        print(
            f"error: isolation-level transaction failed on database "
            f"'{database_id}' in instance '{instance_id}': {message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Previous Title: {previous_title}")
        print(f"Updated Rows: {updated_rows}")


# [END spanner_isolation_level]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Configure client and per-transaction isolation levels in Spanner."
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

    run_transaction_with_isolation_level(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
