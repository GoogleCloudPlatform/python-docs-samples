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

# [START spanner_create_backup]
import datetime
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_admin_database_v1


def create_backup(
    project_id: str, instance_id: str, database_id: str, backup_id: str
) -> None:
    """Creates a point-in-time Cloud Spanner database backup.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The source Spanner database ID.
        backup_id: The new backup ID to create.
    """
    admin_client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = admin_client.instance_path(project_id, instance_id)
    database_path = admin_client.database_path(project_id, instance_id, database_id)
    data_client = spanner.Client(project=project_id)
    database = data_client.instance(instance_id).database(database_id)
    expire_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=7
    )

    try:
        with database.snapshot() as snapshot:
            version_row = next(iter(snapshot.execute_sql("SELECT CURRENT_TIMESTAMP()")))
            version_time = version_row[0]

        backup_pb = spanner_admin_database_v1.Backup(
            database=database_path,
            expire_time=expire_time,
            version_time=version_time,
        )
        request = spanner_admin_database_v1.CreateBackupRequest(
            parent=parent,
            backup_id=backup_id,
            backup=backup_pb,
        )
        operation = admin_client.create_backup(request=request)
        print(f"Waiting for backup '{backup_id}' creation to complete...")
        backup = operation.result(timeout=2100)
    except exceptions.AlreadyExists as err:
        print(
            f"error: backup '{backup_id}' already exists on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on backup '{backup_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create backup '{backup_id}' for database "
            f"'{database_id}' on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {backup_id}")
        print(f"Backup Size Bytes: {backup.size_bytes}")
        print(f"Backup State: {backup.state.name}")


# [END spanner_create_backup]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Create a Spanner database backup.")
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
        default="example-backup",
    )
    args = parser.parse_args()

    create_backup(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        backup_id=args.backup_id,
    )
