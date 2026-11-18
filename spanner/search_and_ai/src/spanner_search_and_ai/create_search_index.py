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

# [START spanner_create_search_index]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_search_index(project_id: str, instance_id: str, database_id: str) -> None:
    """Creates a full-text search index over a TOKENLIST generated column.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Enterprise-edition Spanner instance ID.
        database_id: The Spanner database ID containing the Albums table.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)
    index_name = "AlbumsIndex"

    ddl_statement = (
        f"CREATE SEARCH INDEX {index_name} "
        "ON Albums(AlbumTitle_Tokens) "
        "STORING (AlbumTitle)"
    )
    request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[ddl_statement],
    )

    try:
        operation = client.update_database_ddl(request=request)
        print(f"Waiting for search index '{index_name}' creation to complete...")
        operation.result(timeout=300)
    except (exceptions.AlreadyExists, exceptions.FailedPrecondition) as err:
        print(
            f"error: search index '{index_name}' already exists or preconditions "
            f"failed on database '{database_id}' in instance '{instance_id}': "
            f"{err.message}",
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
            f"error: failed to create search index '{index_name}' on database "
            f"'{database_id}' in instance '{instance_id}'"
            f": {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Index Name: {index_name}")


# [END spanner_create_search_index]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a full-text search index in Spanner."
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

    create_search_index(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
