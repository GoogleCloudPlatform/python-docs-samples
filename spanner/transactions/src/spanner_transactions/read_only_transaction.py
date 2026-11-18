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

# [START spanner_read_only_transaction]
import sys

from google.api_core import exceptions
from google.cloud import spanner


def read_only_transaction(project_id: str, instance_id: str, database_id: str) -> None:
    """Executes consistent multi-statement reads inside a multi-use snapshot.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Albums.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    album_cols = ("SingerId", "AlbumId", "AlbumTitle")
    all_keys = spanner.KeySet(all_=True)

    try:
        with database.snapshot(multi_use=True) as snapshot:
            sql_rows = list(
                snapshot.execute_sql("SELECT SingerId, AlbumId, AlbumTitle FROM Albums")
            )
            key_rows = list(
                snapshot.read(table="Albums", columns=album_cols, keyset=all_keys)
            )
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: read-only transaction failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        for singer_id, album_id, album_title in sql_rows:
            print(f"Album ID: {album_id}, Singer ID: {singer_id}, Title: {album_title}")
        print(f"KeyRead Row Count: {len(key_rows)}")
        print(f"SqlRead Row Count: {len(sql_rows)}")


# [END spanner_read_only_transaction]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run consistent SQL and KeySet reads inside a multi-use read-only transaction."
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

    read_only_transaction(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
