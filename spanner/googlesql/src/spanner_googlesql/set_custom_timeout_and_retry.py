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

# [START spanner_set_custom_timeout_and_retry]
import sys

from google.api_core import exceptions
from google.api_core import retry
from google.cloud import spanner


def set_custom_timeout_and_retry(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Executes a SQL query with custom RPC retry and timeout settings.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Albums table.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    custom_retry = retry.Retry(
        initial=0.5,
        maximum=16.0,
        multiplier=1.5,
        timeout=60.0,
        predicate=retry.if_exception_type(exceptions.ServiceUnavailable),
    )

    try:
        with database.snapshot() as snapshot:
            rows = list(
                snapshot.execute_sql(
                    "SELECT SingerId, AlbumId, AlbumTitle FROM Albums",
                    retry=custom_retry,
                    timeout=60.0,
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
            f"error: query with custom timeout and retry failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        for singer_id, album_id, album_title in rows:
            print(f"Album ID: {album_id}, Singer ID: {singer_id}, Title: {album_title}")
        print(f"Row Count: {len(rows)}")


# [END spanner_set_custom_timeout_and_retry]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run a Spanner SQL query with custom RPC retry and timeout settings."
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

    set_custom_timeout_and_retry(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
