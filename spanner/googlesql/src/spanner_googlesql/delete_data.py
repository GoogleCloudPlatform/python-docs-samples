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

# [START spanner_delete_data]
import sys

from google.api_core import exceptions
from google.cloud import spanner


def delete_data(project_id: str, instance_id: str, database_id: str) -> None:
    """Deletes individual keys, key ranges, and remaining rows via KeySet mutations.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Singers and Albums.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)

    albums_to_delete = spanner.KeySet(keys=[[2, 1], [2, 3]])
    singers_range = spanner.KeyRange(start_closed=[3], end_open=[5])
    singers_to_delete = spanner.KeySet(ranges=[singers_range])
    remaining_singers = spanner.KeySet(all_=True)

    try:
        with database.batch() as specific_batch:
            specific_batch.delete("Albums", albums_to_delete)
            specific_batch.delete("Singers", singers_to_delete)
        with database.batch() as remaining_batch:
            remaining_batch.delete("Singers", remaining_singers)
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: batch delete failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Remaining Rows Committed At: {remaining_batch.committed.isoformat()}")
        print(f"Specific Rows Committed At: {specific_batch.committed.isoformat()}")


# [END spanner_delete_data]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Delete rows and key ranges using KeySet mutations."
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

    delete_data(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
