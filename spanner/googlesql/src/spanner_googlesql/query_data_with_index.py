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

# [START spanner_query_data_with_index]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def query_data_with_index(project_id: str, instance_id: str, database_id: str) -> None:
    """Queries Albums within a title range using an explicit FORCE_INDEX hint.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID with index AlbumsByAlbumTitle.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    params = {"start_title": "Aardvark", "end_title": "Goo"}
    types = {
        "start_title": param_types.STRING,
        "end_title": param_types.STRING,
    }

    try:
        with database.snapshot() as snapshot:
            rows = list(
                snapshot.execute_sql(
                    "SELECT AlbumId, AlbumTitle, MarketingBudget "
                    "FROM Albums@{FORCE_INDEX=AlbumsByAlbumTitle} "
                    "WHERE AlbumTitle >= @start_title AND AlbumTitle < @end_title",
                    params=params,
                    param_types=types,
                )
            )
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: FORCE_INDEX query failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        for album_id, album_title, budget in rows:
            print(f"Album ID: {album_id}, Title: {album_title}, Budget: {budget}")
        print(f"Row Count: {len(rows)}")


# [END spanner_query_data_with_index]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Query Albums using a FORCE_INDEX=AlbumsByAlbumTitle hint."
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

    query_data_with_index(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
