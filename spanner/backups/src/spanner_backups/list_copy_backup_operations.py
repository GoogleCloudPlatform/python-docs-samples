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

# [START spanner_list_copy_backup_operations]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def list_copy_backup_operations(project_id: str, instance_id: str) -> None:
    """Lists copy-backup long-running operations on a destination Spanner instance.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The destination Spanner instance ID.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    request = spanner_admin_database_v1.ListBackupOperationsRequest(
        parent=parent,
        filter="(metadata.@type:type.googleapis.com/google.spanner.admin.database.v1.CopyBackupMetadata)",
    )

    try:
        operations = list(client.list_backup_operations(request=request))
    except exceptions.NotFound as err:
        print(
            f"error: Spanner instance '{instance_id}' was not found: " f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list copy-backup operations on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {instance_id}")
        print(f"Copy Backup Operation Count: {len(operations)}")
        for op in operations:
            meta = spanner_admin_database_v1.CopyBackupMetadata.deserialize(
                op.metadata.value
            )
            print(f"Destination Backup: {meta.name.split('/')[-1]}")
            print(f"Operation Done: {op.done}")
            print(f"Source Backup: {meta.source_backup.split('/')[-1]}")


# [END spanner_list_copy_backup_operations]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="List copy-backup operations on a Cloud Spanner instance."
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
    args = parser.parse_args()

    list_copy_backup_operations(
        project_id=args.project_id,
        instance_id=args.instance_id,
    )
