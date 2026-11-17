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

# [START spanner_dml_last_statement]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1
from google.cloud.spanner_v1 import param_types


def update_dml_last_statement(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Executes the final DML statement in a transaction with last_statement=True.

    Setting last_statement=True piggybacks the transaction commit onto the
    ExecuteSql RPC, saving an extra Commit round trip.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Singers table.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    updated_counts: list[int] = []

    def update_singers(transaction: spanner_v1.Transaction) -> None:
        row_count = transaction.execute_update(
            "UPDATE Singers SET LastName = @last_name WHERE SingerId = @singer_id",
            params={"last_name": "Doe", "singer_id": 54213},
            param_types={
                "last_name": param_types.STRING,
                "singer_id": param_types.INT64,
            },
            last_statement=True,
        )
        updated_counts.append(int(row_count))

    try:
        database.run_in_transaction(update_singers)
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"in project '{project_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: DML last_statement update failed on database "
            f"'{database_id}' in instance '{instance_id}' for project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        print("Last Statement Optimization: True")
        print(f"Updated Rows: {updated_counts[-1]}")


# [END spanner_dml_last_statement]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Execute a GoogleSQL DML update with last_statement=True."
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

    update_dml_last_statement(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
