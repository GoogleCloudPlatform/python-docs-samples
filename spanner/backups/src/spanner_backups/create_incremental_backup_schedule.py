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

# [START spanner_create_incremental_backup_schedule]
import datetime
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_incremental_backup_schedule(
    project_id: str,
    instance_id: str,
    database_id: str,
    schedule_id: str,
) -> None:
    """Creates an incremental backup schedule on an Enterprise Spanner database.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Enterprise Spanner instance ID.
        database_id: The Spanner database ID.
        schedule_id: The new incremental backup schedule ID.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.database_path(project_id, instance_id, database_id)
    cron_spec = spanner_admin_database_v1.CrontabSpec(text="0 */4 * * *")
    schedule_spec = spanner_admin_database_v1.BackupScheduleSpec(cron_spec=cron_spec)
    enc_type = (
        spanner_admin_database_v1.CreateBackupEncryptionConfig.EncryptionType.GOOGLE_DEFAULT_ENCRYPTION
    )
    enc_config = spanner_admin_database_v1.CreateBackupEncryptionConfig(
        encryption_type=enc_type
    )
    schedule_pb = spanner_admin_database_v1.BackupSchedule(
        spec=schedule_spec,
        retention_duration=datetime.timedelta(hours=24),
        encryption_config=enc_config,
        incremental_backup_spec=spanner_admin_database_v1.IncrementalBackupSpec(),
    )
    request = spanner_admin_database_v1.CreateBackupScheduleRequest(
        parent=parent,
        backup_schedule_id=schedule_id,
        backup_schedule=schedule_pb,
    )

    try:
        created = client.create_backup_schedule(request=request)
    except exceptions.AlreadyExists as err:
        print(
            f"error: backup schedule '{schedule_id}' already exists on "
            f"database '{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create incremental backup schedule "
            f"'{schedule_id}' on database '{database_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        retention_hours = int(created.retention_duration.total_seconds() // 3600)
        print(f"Resource ID: {schedule_id}")
        print(f"Cron Expression: {created.spec.cron_spec.text}")
        print(f"Retention Hours: {retention_hours}")


# [END spanner_create_incremental_backup_schedule]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a Spanner incremental backup schedule."
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

    create_incremental_backup_schedule(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        schedule_id=args.schedule_id,
    )
