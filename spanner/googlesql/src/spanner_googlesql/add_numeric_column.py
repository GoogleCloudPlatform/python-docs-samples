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

# [START spanner_add_numeric_column]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def add_numeric_column(project_id: str, instance_id: str, database_id: str) -> None:
    """Adds a GoogleSQL NUMERIC column to the Venues table via DDL.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Venues table.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)
    table_name = "Venues"
    column_name = "Revenue"
    request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[f"ALTER TABLE {table_name} ADD COLUMN {column_name} NUMERIC"],
    )

    try:
        operation = client.update_database_ddl(request=request)
        print(f"Waiting for NUMERIC column '{column_name}' addition...")
        operation.result(timeout=300)
    except (exceptions.AlreadyExists, exceptions.FailedPrecondition) as err:
        print(
            f"error: column '{column_name}' already exists or preconditions "
            f"failed on table '{table_name}' in database '{database_id}' "
            f"on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to add column '{column_name}' on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Added Column: {column_name}")
        print(f"Table Name: {table_name}")


# [END spanner_add_numeric_column]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Add a NUMERIC column to the Venues table."
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

    add_numeric_column(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
