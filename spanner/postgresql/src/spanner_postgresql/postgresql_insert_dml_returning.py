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

# [START spanner_postgresql_insert_dml_returning]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def postgresql_insert_dml_returning(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Inserts Singers rows in PostgreSQL Spanner and returns FullName values.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The PostgreSQL-dialect Spanner database ID.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    inserted_names: list[str] = []
    row_counts: list[int] = []

    def insert_singers(transaction: spanner_v1.Transaction) -> None:
        inserted_names.clear()
        row_counts.clear()
        results = transaction.execute_sql(
            "INSERT INTO Singers (SingerId, FirstName, LastName) VALUES "
            "(21, 'Luann', 'Chizoba'), "
            "(22, 'Denis', 'Patricio'), "
            "(23, 'Felix', 'Ronan'), "
            "(24, 'Dominik', 'Martyna') "
            "RETURNING FullName"
        )
        for row in results:
            inserted_names.append(str(row[0]))
        row_counts.append(int(results.stats.row_count_exact))

    try:
        database.run_in_transaction(insert_singers)
    except exceptions.AlreadyExists as err:
        print(
            f"error: one or more SingerId rows already exist in PostgreSQL "
            f"database '{database_id}' on instance '{instance_id}' in project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: PostgreSQL INSERT RETURNING failed on database "
            f"'{database_id}' in instance '{instance_id}' for project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for full_name in inserted_names:
            print(f"Full Name: {full_name}")
        print(f"Inserted Rows: {row_counts[-1]}")


# [END spanner_postgresql_insert_dml_returning]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Insert Singers rows using PostgreSQL-dialect DML RETURNING."
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

    postgresql_insert_dml_returning(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
