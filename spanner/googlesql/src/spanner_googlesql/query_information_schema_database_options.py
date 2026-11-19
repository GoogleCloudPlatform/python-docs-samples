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

# [START spanner_query_information_schema_database_options]
import sys

from google.api_core import exceptions
from google.cloud import spanner


def query_information_schema_database_options(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Queries INFORMATION_SCHEMA.DATABASE_OPTIONS for the default_leader setting.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    sql = """
        SELECT OPTION_VALUE AS default_leader
        FROM INFORMATION_SCHEMA.DATABASE_OPTIONS
        WHERE SCHEMA_NAME = '' AND OPTION_NAME = 'default_leader'
    """

    try:
        with database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(sql))
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: INFORMATION_SCHEMA query failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        default_leader = str(rows[0][0]) if rows else "not configured"
        print(f"Resource ID: {database_id}")
        print(f"Default Leader: {default_leader}")
        print(f"Option Rows Found: {len(rows)}")


# [END spanner_query_information_schema_database_options]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Query INFORMATION_SCHEMA.DATABASE_OPTIONS for default_leader."
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

    query_information_schema_database_options(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
