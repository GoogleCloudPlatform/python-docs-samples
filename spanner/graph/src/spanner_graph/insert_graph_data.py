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

# [START spanner_insert_graph_data]
import sys

from google.api_core import exceptions
from google.cloud import spanner


def insert_graph_data(project_id: str, instance_id: str, database_id: str) -> None:
    """Inserts node and edge rows into FinGraph tables via batch mutations.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing FinGraph tables.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    accounts = [
        (7, "2020-01-10T06:22:20.12Z", False, "Vacation Fund"),
        (16, "2020-01-27T17:55:09.12Z", True, "Vacation Fund"),
        (20, "2020-02-18T05:44:20.12Z", False, "Rainy Day Fund"),
    ]
    persons = [
        (1, "Alex", "1991-12-21T00:00:00.12Z", "Australia", "Adelaide"),
        (2, "Dana", "1980-10-31T00:00:00.12Z", "Czech_Republic", "Moravia"),
        (3, "Lee", "1986-12-07T00:00:00.12Z", "India", "Kollam"),
    ]
    transfers = [
        (7, 16, 300.0, "2020-08-29T15:28:58.12Z", "304330008004315"),
        (7, 16, 100.0, "2020-10-04T16:55:05.12Z", "304120005529714"),
        (16, 20, 300.0, "2020-09-25T02:36:14.12Z", "103650009791820"),
        (20, 7, 500.0, "2020-10-04T16:55:05.12Z", "304120005529714"),
        (20, 16, 200.0, "2020-10-17T03:59:40.12Z", "302290001255747"),
    ]
    ownerships = [
        (1, 7, "2020-01-10T06:22:20.12Z"),
        (2, 20, "2020-01-27T17:55:09.12Z"),
        (3, 16, "2020-02-18T05:44:20.12Z"),
    ]

    try:
        with database.batch() as batch:
            batch.insert(
                table="Account",
                columns=("id", "create_time", "is_blocked", "nick_name"),
                values=accounts,
            )
            batch.insert(
                table="Person",
                columns=("id", "name", "birthday", "country", "city"),
                values=persons,
            )
            batch.insert(
                table="AccountTransferAccount",
                columns=("id", "to_id", "amount", "create_time", "order_number"),
                values=transfers,
            )
            batch.insert(
                table="PersonOwnAccount",
                columns=("id", "account_id", "create_time"),
                values=ownerships,
            )
    except exceptions.AlreadyExists as err:
        print(
            f"error: graph node or edge rows already exist on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: graph mutation insert failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Committed At: {batch.committed.isoformat()}")
        print(f"InsertedEdges: {len(transfers) + len(ownerships)}")
        print(f"InsertedNodes: {len(accounts) + len(persons)}")


# [END spanner_insert_graph_data]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Insert FinGraph node and edge rows using mutations."
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

    insert_graph_data(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
