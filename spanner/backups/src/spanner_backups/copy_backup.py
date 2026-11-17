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

# [START spanner_copy_backup]
from datetime import datetime, timedelta, timezone
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def copy_backup(
    project_id: str,
    instance_id: str,
    backup_id: str,
    source_backup_path: str,
) -> None:
    """Copies an existing Spanner backup to a destination instance.

    Args:
        project_id: The destination Google Cloud project ID.
        instance_id: The destination Spanner instance ID.
        backup_id: The ID for the newly copied backup.
        source_backup_path: Full resource path of the source backup
            (projects/<proj>/instances/<inst>/backups/<backup>).
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    expire_time = datetime.now(timezone.utc) + timedelta(days=14)

    request = spanner_admin_database_v1.CopyBackupRequest(
        parent=parent,
        backup_id=backup_id,
        source_backup=source_backup_path,
        expire_time=expire_time,
    )

    try:
        operation = client.copy_backup(request=request)
        print(f"Waiting for backup copy '{backup_id}' to complete...")
        copied = operation.result(timeout=2100)
    except exceptions.AlreadyExists as err:
        print(
            f"error: backup '{backup_id}' already exists on instance "
            f"'{instance_id}' in project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.NotFound as err:
        print(
            f"error: source backup '{source_backup_path}' or destination "
            f"instance '{instance_id}' in project '{project_id}' was not found: "
            f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to copy backup '{source_backup_path}' to "
            f"'{backup_id}' on instance '{instance_id}' in project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {copied.name}")
        print(f"Backup State: {copied.state.name}")
        print(f"Size Bytes: {copied.size_bytes}")


# [END spanner_copy_backup]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Copy an existing Cloud Spanner backup."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Destination Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
        help="Destination Spanner instance ID (default: $SPANNER_INSTANCE_ID)",
    )
    parser.add_argument(
        "--backup-id",
        default=os.environ.get("SPANNER_BACKUP_ID", "example-copied-backup"),
        help="New copied backup ID (default: $SPANNER_BACKUP_ID)",
    )
    parser.add_argument(
        "--source-backup-path",
        default=os.environ.get(
            "SPANNER_SOURCE_BACKUP_PATH",
            "projects/example-project-id/instances/example-instance/backups/example-source-backup",
        ),
        help="Full resource path of the source backup",
    )
    args = parser.parse_args()

    copy_backup(
        project_id=args.project_id,
        instance_id=args.instance_id,
        backup_id=args.backup_id,
        source_backup_path=args.source_backup_path,
    )
