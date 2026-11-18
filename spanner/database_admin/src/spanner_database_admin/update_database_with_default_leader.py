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

# [START spanner_update_database_with_default_leader]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def update_database_with_default_leader(
    project_id: str, instance_id: str, database_id: str, default_leader: str
) -> None:
    """Updates the default_leader database option via ALTER DATABASE DDL.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The multi-region Spanner instance ID.
        database_id: The Spanner database ID.
        default_leader: The target leader region (for example, 'us-central1').
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)
    request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[
            f"ALTER DATABASE `{database_id}` "
            f"SET OPTIONS (default_leader = '{default_leader}')"
        ],
    )

    try:
        operation = client.update_database_ddl(request=request)
        print(
            f"Waiting for default_leader update to '{default_leader}' on "
            f"'{database_id}'..."
        )
        operation.result(timeout=300)
        updated_db = client.get_database(name=database_path)
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
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
            f"error: failed to update default_leader on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Default Leader: {updated_db.default_leader}")


# [END spanner_update_database_with_default_leader]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Update the default_leader option on a Spanner database."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_MR_INSTANCE_ID", "example-mr-instance"),
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
    )
    parser.add_argument(
        "--default-leader",
        default=os.environ.get("SPANNER_DEFAULT_LEADER", "us-central1"),
    )
    args = parser.parse_args()

    update_database_with_default_leader(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        default_leader=args.default_leader,
    )
