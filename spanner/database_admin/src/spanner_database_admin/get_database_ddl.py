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

# [START spanner_get_database_ddl]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def get_database_ddl(project_id: str, instance_id: str, database_id: str) -> None:
    """Retrieves and prints the schema DDL statements for a Spanner database.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)

    try:
        ddl_response = client.get_database_ddl(database=database_path)
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to retrieve DDL for database '{database_id}' "
            f"on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        statements = list(ddl_response.statements)
        print(f"Resource ID: {database_id}")
        for statement in statements:
            first_line = statement.strip().splitlines()[0]
            print(f"DDL Statement: {first_line}")
        print(f"Statement Count: {len(statements)}")


# [END spanner_get_database_ddl]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Retrieve schema DDL statements for a Spanner database."
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

    get_database_ddl(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
