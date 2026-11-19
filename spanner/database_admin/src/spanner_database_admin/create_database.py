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

# [START spanner_create_database]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_database(project_id: str, instance_id: str, database_id: str) -> None:
    """Creates a GoogleSQL Spanner database with Singers and Albums tables.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The new Spanner database ID to create.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    request = spanner_admin_database_v1.CreateDatabaseRequest(
        parent=parent,
        create_statement=f"CREATE DATABASE `{database_id}`",
        extra_statements=[
            """
            CREATE TABLE Singers (
              SingerId INT64 NOT NULL,
              FirstName STRING(1024),
              LastName STRING(1024),
              SingerInfo BYTES(MAX),
              FullName STRING(2048) AS (
                ARRAY_TO_STRING([FirstName, LastName], ' ')
              ) STORED
            ) PRIMARY KEY (SingerId)
            """,
            """
            CREATE TABLE Albums (
              SingerId INT64 NOT NULL,
              AlbumId INT64 NOT NULL,
              AlbumTitle STRING(MAX)
            ) PRIMARY KEY (SingerId, AlbumId),
              INTERLEAVE IN PARENT Singers ON DELETE CASCADE
            """,
        ],
    )

    try:
        operation = client.create_database(request=request)
        print(f"Waiting for database '{database_id}' creation to complete...")
        database = operation.result(timeout=300)
    except exceptions.AlreadyExists as err:
        print(
            f"error: database '{database_id}' already exists on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on database '{database_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create database '{database_id}' on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Database State: {database.state.name}")


# [END spanner_create_database]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a GoogleSQL Spanner database and tables."
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

    create_database(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
