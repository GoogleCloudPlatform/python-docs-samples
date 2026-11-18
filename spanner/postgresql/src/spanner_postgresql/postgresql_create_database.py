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

# [START spanner_postgresql_create_database]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_postgresql_database(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Creates a PostgreSQL-dialect Spanner database and initial Singers/Albums DDL.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The new PostgreSQL-dialect database ID to create.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    database_path = client.database_path(project_id, instance_id, database_id)
    create_request = spanner_admin_database_v1.CreateDatabaseRequest(
        parent=parent,
        create_statement=f'CREATE DATABASE "{database_id}"',
        database_dialect=spanner_admin_database_v1.DatabaseDialect.POSTGRESQL,
    )
    ddl_request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[
            "CREATE TABLE Singers ("
            "  SingerId bigint NOT NULL,"
            "  FirstName character varying(1024),"
            "  LastName character varying(1024),"
            "  SingerInfo bytea,"
            "  FullName character varying(2048) "
            "    GENERATED ALWAYS AS (FirstName || ' ' || LastName) STORED,"
            "  PRIMARY KEY (SingerId)"
            ")",
            "CREATE TABLE Albums ("
            "  SingerId bigint NOT NULL,"
            "  AlbumId bigint NOT NULL,"
            "  AlbumTitle character varying(1024),"
            "  PRIMARY KEY (SingerId, AlbumId)"
            ") INTERLEAVE IN PARENT Singers ON DELETE CASCADE",
        ],
    )

    try:
        create_op = client.create_database(request=create_request)
        print(f"Waiting for PostgreSQL database '{database_id}' creation...")
        database = create_op.result(timeout=300)
        ddl_op = client.update_database_ddl(request=ddl_request)
        print(f"Waiting for Singers and Albums DDL on '{database_id}'...")
        ddl_op.result(timeout=300)
    except exceptions.AlreadyExists as err:
        print(
            f"error: database '{database_id}' already exists on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create PostgreSQL database '{database_id}' "
            f"on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Database Dialect: {database.database_dialect.name}")


# [END spanner_postgresql_create_database]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a PostgreSQL-dialect Spanner database and initial tables."
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
        default=os.environ.get("SPANNER_PG_DATABASE_ID", "example-db"),
        help="Spanner database ID",
    )
    args = parser.parse_args()

    create_postgresql_database(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
