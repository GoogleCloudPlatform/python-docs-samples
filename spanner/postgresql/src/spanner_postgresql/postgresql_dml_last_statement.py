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

# [START spanner_postgresql_dml_last_statement]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1
from google.cloud.spanner_v1 import param_types


def update_postgresql_dml_last_statement(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Executes the final PostgreSQL DML statement with last_statement=True.

    Setting last_statement=True commits the transaction inline with the final
    DML request, avoiding a separate Commit RPC round trip.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The PostgreSQL-dialect Spanner database ID.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    updated_count = 0

    def update_singers(transaction: spanner_v1.Transaction) -> None:
        nonlocal updated_count
        row_count = transaction.execute_update(
            "UPDATE Singers SET LastName = $1 WHERE SingerId = $2",
            params={"p1": "Doe", "p2": 54214},
            param_types={"p1": param_types.STRING, "p2": param_types.INT64},
            last_statement=True,
        )
        updated_count = int(row_count)

    try:
        database.run_in_transaction(update_singers)
    except exceptions.NotFound as err:
        print(
            f"error: PostgreSQL database '{database_id}' on instance "
            f"'{instance_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: PostgreSQL DML last_statement update failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Updated Rows: {updated_count}")


# [END spanner_postgresql_dml_last_statement]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Execute a PostgreSQL-dialect DML update with last_statement=True."
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
        default=os.environ.get("SPANNER_DATABASE_ID", "example-pg-db"),
        help="PostgreSQL-dialect Spanner database ID (default: $SPANNER_DATABASE_ID)",
    )
    args = parser.parse_args()

    update_postgresql_dml_last_statement(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
