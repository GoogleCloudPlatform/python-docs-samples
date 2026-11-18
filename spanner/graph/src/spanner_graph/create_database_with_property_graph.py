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

# [START spanner_create_database_with_property_graph]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_database_with_property_graph(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Creates a Spanner database with node/edge tables and FinGraph DDL.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The new Spanner database ID to create.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    ddl_statements = [
        "CREATE TABLE Person ("
        "  id INT64 NOT NULL,"
        "  name STRING(MAX),"
        "  birthday TIMESTAMP,"
        "  country STRING(MAX),"
        "  city STRING(MAX)"
        ") PRIMARY KEY (id)",
        "CREATE TABLE Account ("
        "  id INT64 NOT NULL,"
        "  create_time TIMESTAMP,"
        "  is_blocked BOOL,"
        "  nick_name STRING(MAX)"
        ") PRIMARY KEY (id)",
        "CREATE TABLE PersonOwnAccount ("
        "  id INT64 NOT NULL,"
        "  account_id INT64 NOT NULL,"
        "  create_time TIMESTAMP,"
        "  FOREIGN KEY (account_id) REFERENCES Account (id)"
        ") PRIMARY KEY (id, account_id),"
        "  INTERLEAVE IN PARENT Person ON DELETE CASCADE",
        "CREATE TABLE AccountTransferAccount ("
        "  id INT64 NOT NULL,"
        "  to_id INT64 NOT NULL,"
        "  amount FLOAT64,"
        "  create_time TIMESTAMP NOT NULL,"
        "  order_number STRING(MAX),"
        "  FOREIGN KEY (to_id) REFERENCES Account (id)"
        ") PRIMARY KEY (id, to_id, create_time),"
        "  INTERLEAVE IN PARENT Account ON DELETE CASCADE",
        "CREATE OR REPLACE PROPERTY GRAPH FinGraph "
        "NODE TABLES (Account, Person) "
        "EDGE TABLES ("
        "  PersonOwnAccount "
        "    SOURCE KEY (id) REFERENCES Person (id) "
        "    DESTINATION KEY (account_id) REFERENCES Account (id) "
        "    LABEL Owns, "
        "  AccountTransferAccount "
        "    SOURCE KEY (id) REFERENCES Account (id) "
        "    DESTINATION KEY (to_id) REFERENCES Account (id) "
        "    LABEL Transfers"
        ")",
    ]
    request = spanner_admin_database_v1.CreateDatabaseRequest(
        parent=parent,
        create_statement=f"CREATE DATABASE `{database_id}`",
        extra_statements=ddl_statements,
    )

    try:
        operation = client.create_database(request=request)
        print(f"Waiting for property-graph database '{database_id}' creation...")
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
            f"error: failed to create property-graph database '{database_id}' "
            f"on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Database State: {database.state.name}")


# [END spanner_create_database_with_property_graph]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a Spanner database with FinGraph property-graph schema."
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

    create_database_with_property_graph(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
