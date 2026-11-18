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

# [START spanner_batch_write_at_least_once]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def batch_write_at_least_once(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Applies independent mutation groups non-atomically via BatchWrite.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Singers and Albums.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    singer_cols = ("SingerId", "FirstName", "LastName")
    album_cols = ("SingerId", "AlbumId", "AlbumTitle")
    group1_singers = [(16, "Scarlet", "Terry")]
    group2_singers = [(17, "Marc", ""), (18, "Catalina", "Smith")]
    group2_albums = [(17, 1, "Total Junk"), (18, 2, "Go, Go, Go")]
    applied_groups: list[tuple[list[int], object]] = []
    failed_groups: list[tuple[list[int], int]] = []

    def record_response(response: spanner_v1.BatchWriteResponse) -> None:
        indexes = list(response.indexes)
        if response.status.code == 0:
            applied_groups.append((indexes, response.commit_timestamp))
        else:
            failed_groups.append((indexes, response.status.code))

    def execute_batch_groups() -> None:
        with database.mutation_groups() as groups:
            group1 = groups.group()
            group1.insert_or_update(
                table="Singers", columns=singer_cols, values=group1_singers
            )
            group2 = groups.group()
            group2.insert_or_update(
                table="Singers", columns=singer_cols, values=group2_singers
            )
            group2.insert_or_update(
                table="Albums", columns=album_cols, values=group2_albums
            )
            responses = list(groups.batch_write())
        for response in responses:
            record_response(response)

    try:
        execute_batch_groups()
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: BatchWrite RPC failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        for indexes, commit_ts in applied_groups:
            print(f"Applied Group Indexes: {indexes}, Committed At: {commit_ts}")
        print(f"Total Groups Processed: {len(applied_groups) + len(failed_groups)}")


# [END spanner_batch_write_at_least_once]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Write independent mutation groups using the Spanner BatchWrite API."
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

    batch_write_at_least_once(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
