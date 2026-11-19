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

# [START spanner_insert_data]
import sys

from google.api_core import exceptions
from google.cloud import spanner


def insert_data(project_id: str, instance_id: str, database_id: str) -> None:
    """Inserts sample Singers and Albums rows using the Spanner Mutation API.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID with empty Singers and Albums tables.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    singer_rows = [
        (1, "Marc", "Richards"),
        (2, "Catalina", "Smith"),
        (3, "Alice", "Trentor"),
        (4, "Lea", "Martin"),
        (5, "David", "Lomond"),
    ]
    album_rows = [
        (1, 1, "Total Junk"),
        (1, 2, "Go, Go, Go"),
        (2, 1, "Green"),
        (2, 2, "Forever Hold Your Peace"),
        (2, 3, "Terrified"),
    ]

    try:
        with database.batch() as batch:
            batch.insert(
                table="Singers",
                columns=("SingerId", "FirstName", "LastName"),
                values=singer_rows,
            )
            batch.insert(
                table="Albums",
                columns=("SingerId", "AlbumId", "AlbumTitle"),
                values=album_rows,
            )
    except exceptions.AlreadyExists as err:
        print(
            f"error: one or more Singers or Albums rows already exist on "
            f"database '{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: batch insert failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Inserted Albums: {len(album_rows)}")
        print(f"Inserted Singers: {len(singer_rows)}")


# [END spanner_insert_data]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Insert sample rows into Singers and Albums."
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

    insert_data(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
