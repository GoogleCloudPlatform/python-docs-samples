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

# [START spanner_list_databases]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def list_databases(project_id: str, instance_id: str) -> None:
    """Lists all Spanner databases and their leader options on an instance.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    request = spanner_admin_database_v1.ListDatabasesRequest(parent=parent)

    try:
        databases = list(client.list_databases(request=request))
    except exceptions.NotFound as err:
        print(
            f"error: instance '{instance_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list databases on instance '{instance_id}': "
            f"{err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {instance_id}")
        print(f"Database Count: {len(databases)}")
        for db in databases:
            db_id = db.name.split("/")[-1]
            leader = db.default_leader or "regional-default"
            print(f"Database ID: {db_id}, Default Leader: {leader}")


# [END spanner_list_databases]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="List Spanner databases on an instance."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
    )
    args = parser.parse_args()

    list_databases(project_id=args.project_id, instance_id=args.instance_id)
