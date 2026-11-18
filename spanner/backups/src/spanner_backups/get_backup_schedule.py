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

# [START spanner_get_backup_schedule]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def get_backup_schedule(
    project_id: str,
    instance_id: str,
    database_id: str,
    schedule_id: str,
) -> None:
    """Retrieves metadata for a Cloud Spanner backup schedule.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID.
        schedule_id: The backup schedule ID to inspect.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    schedule_path = client.backup_schedule_path(
        project_id, instance_id, database_id, schedule_id
    )
    request = spanner_admin_database_v1.GetBackupScheduleRequest(name=schedule_path)

    try:
        schedule = client.get_backup_schedule(request=request)
    except exceptions.NotFound as err:
        print(
            f"error: backup schedule '{schedule_id}' on database "
            f"'{database_id}' in instance '{instance_id}' was not found: "
            f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to get backup schedule '{schedule_id}' on "
            f"database '{database_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        retention_hours = int(schedule.retention_duration.total_seconds() // 3600)
        print(f"Resource ID: {schedule_id}")
        print(f"Cron Expression: {schedule.spec.cron_spec.text}")
        print(f"Retention Hours: {retention_hours}")


# [END spanner_get_backup_schedule]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Retrieve metadata for a Spanner backup schedule."
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
    parser.add_argument(
        "--schedule-id",
        default="example-backup-schedule",
    )
    args = parser.parse_args()

    get_backup_schedule(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        schedule_id=args.schedule_id,
    )
