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

# [START spanner_list_backup_operations]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def list_backup_operations(
    project_id: str, instance_id: str, database_id: str, backup_id: str
) -> None:
    """Lists CreateBackup and CopyBackup long-running operations on an instance.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The source database ID filter for CreateBackupMetadata.
        backup_id: The source backup ID filter for CopyBackupMetadata.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    create_filter = (
        "(metadata.@type:type.googleapis.com/"
        "google.spanner.admin.database.v1.CreateBackupMetadata) "
        f"AND (metadata.database:{database_id})"
    )
    copy_filter = (
        "(metadata.@type:type.googleapis.com/"
        "google.spanner.admin.database.v1.CopyBackupMetadata) "
        f"AND (metadata.source_backup:{backup_id})"
    )
    create_req = spanner_admin_database_v1.ListBackupOperationsRequest(
        parent=parent, filter=create_filter
    )
    copy_req = spanner_admin_database_v1.ListBackupOperationsRequest(
        parent=parent, filter=copy_filter
    )

    try:
        create_ops = list(client.list_backup_operations(request=create_req))
        copy_ops = list(client.list_backup_operations(request=copy_req))
    except exceptions.NotFound as err:
        print(
            f"error: instance '{instance_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list backup operations on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {instance_id}")
        for op in copy_ops:
            c_meta = spanner_admin_database_v1.CopyBackupMetadata.deserialize(
                op.metadata.value
            )
            dst_id = c_meta.name.split("/")[-1]
            print(
                f"Copy Backup ID: {dst_id}, "
                f"Progress: {c_meta.progress.progress_percent}%"
            )
        print(f"Copy Operations Count: {len(copy_ops)}")
        for op in create_ops:
            b_meta = spanner_admin_database_v1.CreateBackupMetadata.deserialize(
                op.metadata.value
            )
            bkp_id = b_meta.name.split("/")[-1]
            print(
                f"Create Backup ID: {bkp_id}, "
                f"Progress: {b_meta.progress.progress_percent}%"
            )
        print(f"Create Operations Count: {len(create_ops)}")


# [END spanner_list_backup_operations]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="List CreateBackup and CopyBackup operations on an instance."
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
        "--backup-id",
        default=os.environ.get("SPANNER_BACKUP_ID", "example-backup"),
    )
    args = parser.parse_args()

    list_backup_operations(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        backup_id=args.backup_id,
    )
