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

# [START spanner_delete_backup]
import sys
import time

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def delete_backup(project_id: str, instance_id: str, backup_id: str) -> None:
    """Waits for referencing databases to finish optimizing and deletes a backup.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        backup_id: The backup ID to delete.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    backup_path = client.backup_path(project_id, instance_id, backup_id)
    get_request = spanner_admin_database_v1.GetBackupRequest(name=backup_path)
    delete_request = spanner_admin_database_v1.DeleteBackupRequest(name=backup_path)

    def wait_until_unreferenced() -> None:
        backup = client.get_backup(request=get_request)
        while backup.referencing_databases:
            time.sleep(10)
            backup = client.get_backup(request=get_request)

    try:
        wait_until_unreferenced()
        client.delete_backup(request=delete_request)
    except exceptions.NotFound as err:
        print(
            f"error: backup '{backup_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to delete backup '{backup_id}' on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {backup_id}")
        print(f"Deleted Backup: {backup_id}")


# [END spanner_delete_backup]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Delete a Spanner database backup.")
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
    )
    parser.add_argument(
        "--backup-id",
        default=os.environ.get("SPANNER_DISPOSABLE_BACKUP_ID", "example-backup"),
    )
    args = parser.parse_args()

    delete_backup(
        project_id=args.project_id,
        instance_id=args.instance_id,
        backup_id=args.backup_id,
    )
