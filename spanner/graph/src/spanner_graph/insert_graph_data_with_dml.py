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

# [START spanner_insert_graph_data_with_dml]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def insert_graph_data_with_dml(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Inserts Account nodes and AccountTransferAccount edges using DML.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing FinGraph tables.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    inserted_accounts = 0
    inserted_transfers = 0

    def insert_accounts(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal inserted_accounts
        inserted_accounts = transaction.execute_update(
            "INSERT INTO Account (id, create_time, is_blocked) VALUES "
            "(1, CAST('2000-08-10 08:18:48.463959-07:52' AS TIMESTAMP), false), "
            "(2, CAST('2000-08-12 07:13:16.463959-03:41' AS TIMESTAMP), true)"
        )

    def insert_transfers(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal inserted_transfers
        inserted_transfers = transaction.execute_update(
            "INSERT INTO AccountTransferAccount (id, to_id, create_time, amount) "
            "VALUES "
            "(1, 2, CAST('2000-09-11 03:11:18.463959-06:36' AS TIMESTAMP), 100), "
            "(1, 1, CAST('2000-09-12 04:09:34.463959-05:12' AS TIMESTAMP), 200)"
        )

    try:
        database.run_in_transaction(insert_accounts)
        database.run_in_transaction(insert_transfers)
    except exceptions.AlreadyExists as err:
        print(
            f"error: graph rows already exist on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: graph DML insert failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Inserted Accounts: {inserted_accounts}")
        print(f"Inserted Transfers: {inserted_transfers}")


# [END spanner_insert_graph_data_with_dml]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Insert FinGraph nodes and edges via DML."
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
        help="Spanner database ID",
    )
    args = parser.parse_args()

    insert_graph_data_with_dml(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
