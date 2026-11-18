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

# [START spanner_postgresql_create_sequence]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_admin_database_v1
from google.cloud import spanner_v1


def create_postgresql_sequence(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Creates a bit-reversed PostgreSQL sequence and inserts rows via RETURNING.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The PostgreSQL-dialect Spanner database ID.
    """
    admin_client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = admin_client.database_path(project_id, instance_id, database_id)
    ddl_request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[
            "CREATE SEQUENCE Seq BIT_REVERSED_POSITIVE",
            "CREATE TABLE Customers ("
            "  CustomerId bigint DEFAULT nextval('Seq'),"
            "  CustomerName character varying(1024),"
            "  PRIMARY KEY (CustomerId)"
            ")",
        ],
    )
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    customer_ids: list[int] = []

    def insert_customers(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal customer_ids
        rows = list(
            transaction.execute_sql(
                "INSERT INTO Customers (CustomerName) VALUES "
                "('Alice'), ('David'), ('Marc') "
                "RETURNING CustomerId"
            )
        )
        customer_ids = [int(row[0]) for row in rows]

    try:
        operation = admin_client.update_database_ddl(request=ddl_request)
        print(f"Waiting for PostgreSQL sequence 'Seq' creation on '{database_id}'...")
        operation.result(timeout=300)
        database.run_in_transaction(insert_customers)
    except (exceptions.AlreadyExists, exceptions.FailedPrecondition) as err:
        print(
            f"error: sequence 'Seq' or table 'Customers' already exists on "
            f"database '{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create PostgreSQL sequence on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        for cid in customer_ids:
            print(f"Customer ID: {cid}")
        print(f"Inserted Customers: {len(customer_ids)}")


# [END spanner_postgresql_create_sequence]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a bit-reversed PostgreSQL sequence and insert Customers rows."
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

    create_postgresql_sequence(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
