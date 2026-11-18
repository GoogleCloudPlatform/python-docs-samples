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

# [START spanner_database_add_split_points]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def add_split_points(project_id: str, instance_id: str, database_id: str) -> None:
    """Pre-splits a Spanner table and secondary index via AddSplitPoints.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Singers.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)
    index_name = "SingersByFirstLastName"
    ddl_request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[
            f"CREATE INDEX IF NOT EXISTS {index_name} "
            "ON Singers(FirstName, LastName)"
        ],
    )

    table_key = spanner_admin_database_v1.SplitPoints.Key(key_parts=["42"])
    idx_only_key = spanner_admin_database_v1.SplitPoints.Key(key_parts=["John", "Doe"])
    idx_prefix_key = spanner_admin_database_v1.SplitPoints.Key(
        key_parts=["Jane", "Doe"]
    )
    idx_table_key = spanner_admin_database_v1.SplitPoints.Key(key_parts=["38"])

    split_points = [
        spanner_admin_database_v1.SplitPoints(table="Singers", keys=[table_key]),
        spanner_admin_database_v1.SplitPoints(index=index_name, keys=[idx_only_key]),
        spanner_admin_database_v1.SplitPoints(
            index=index_name, keys=[idx_prefix_key, idx_table_key]
        ),
    ]
    split_request = spanner_admin_database_v1.AddSplitPointsRequest(
        database=database_path,
        split_points=split_points,
    )

    try:
        ddl_op = client.update_database_ddl(request=ddl_request)
        print(f"Waiting for index '{index_name}' before adding split points...")
        ddl_op.result(timeout=300)
        client.add_split_points(request=split_request)
    except exceptions.ResourceExhausted as err:
        print(
            f"error: split-point quota exceeded on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
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
            f"error: failed to add split points on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Split Points Added: {len(split_points)}")


# [END spanner_database_add_split_points]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Add table and index split points to a Spanner database."
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

    add_split_points(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
