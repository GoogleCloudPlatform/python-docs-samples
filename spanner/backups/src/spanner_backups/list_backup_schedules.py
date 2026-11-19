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

# [START spanner_list_backup_schedules]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def list_backup_schedules(project_id: str, instance_id: str, database_id: str) -> None:
    """Lists all backup schedules configured on a Cloud Spanner database.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.database_path(project_id, instance_id, database_id)
    request = spanner_admin_database_v1.ListBackupSchedulesRequest(parent=parent)

    try:
        schedules = list(client.list_backup_schedules(request=request))
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list backup schedules on database "
            f"'{database_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Schedule Count: {len(schedules)}")
        for sched in schedules:
            sched_id = sched.name.split("/")[-1]
            print(f"Schedule ID: {sched_id}, " f"Cron: {sched.spec.cron_spec.text}")


# [END spanner_list_backup_schedules]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="List backup schedules on a Spanner database."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
    )
    args = parser.parse_args()

    list_backup_schedules(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
