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

# [START spanner_connect_emulator]
import os
import sys

from google.api_core import exceptions
from google.cloud import spanner


def connect_with_emulator(project_id: str, instance_id: str, database_id: str) -> None:
    """Connects to the Spanner Emulator, provisions schema, and runs a query.

    Requires SPANNER_EMULATOR_HOST (such as 'localhost:9010') to be set in the
    process environment before creating spanner.Client.

    Args:
        project_id: A local project identifier for the emulator.
        instance_id: The emulator Spanner instance ID to create or reuse.
        database_id: The emulator Spanner database ID to create or reuse.
    """
    emulator_host = os.environ.get("SPANNER_EMULATOR_HOST", "")
    client = spanner.Client(project=project_id)
    config_name = f"{client.project_name}/instanceConfigs/emulator-config"
    instance = client.instance(
        instance_id,
        configuration_name=config_name,
        display_name="Example Emulator Instance",
        node_count=1,
    )
    ddl_statements = [
        "CREATE TABLE IF NOT EXISTS Singers ("
        "  SingerId INT64 NOT NULL,"
        "  FirstName STRING(1024),"
        "  LastName STRING(1024)"
        ") PRIMARY KEY (SingerId)"
    ]

    try:
        if not instance.exists():
            print(f"Creating emulator instance '{instance_id}'...")
            instance.create().result(timeout=60)

        database = instance.database(database_id, ddl_statements=ddl_statements)
        if not database.exists():
            print(f"Creating emulator database '{database_id}'...")
            database.create().result(timeout=60)

        with database.snapshot() as snapshot:
            row = list(snapshot.execute_sql("SELECT 1"))[0]
    except exceptions.AlreadyExists as err:
        print(
            f"error: emulator resource already exists for database "
            f"'{database_id}' in instance '{instance_id}' and project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to connect to Spanner Emulator at '{emulator_host}' "
            f"for database '{database_id}' in instance '{instance_id}' and "
            f"project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        print(f"Emulator Host: {emulator_host}")
        print(f"Query Check: {row[0]}")


# [END spanner_connect_emulator]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Connect to the local Spanner Emulator and run a sanity query."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Project ID for the emulator (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
        help="Emulator instance ID (default: $SPANNER_INSTANCE_ID)",
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
        help="Emulator database ID (default: $SPANNER_DATABASE_ID)",
    )
    args = parser.parse_args()

    connect_with_emulator(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
