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

# [START spanner_restore_backup_with_encryption_key]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def restore_backup_with_encryption_key(
    project_id: str,
    instance_id: str,
    new_database_id: str,
    backup_id: str,
    kms_key_name: str,
) -> None:
    """Restores a Spanner backup into a CMEK-encrypted database.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        new_database_id: The new target database ID.
        backup_id: The source backup ID.
        kms_key_name: The Cloud KMS CryptoKey resource path.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    backup_path = client.backup_path(project_id, instance_id, backup_id)
    enc_type = (
        spanner_admin_database_v1.RestoreDatabaseEncryptionConfig.EncryptionType.CUSTOMER_MANAGED_ENCRYPTION
    )
    encryption_config = spanner_admin_database_v1.RestoreDatabaseEncryptionConfig(
        encryption_type=enc_type,
        kms_key_name=kms_key_name,
    )
    request = spanner_admin_database_v1.RestoreDatabaseRequest(
        parent=parent,
        database_id=new_database_id,
        backup=backup_path,
        encryption_config=encryption_config,
    )

    try:
        operation = client.restore_database(request=request)
        print(
            f"Waiting for CMEK restore of '{backup_id}' to " f"'{new_database_id}'..."
        )
        restored = operation.result(timeout=1600)
    except exceptions.AlreadyExists as err:
        print(
            f"error: target database '{new_database_id}' already exists on "
            f"instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on "
            f"new database '{new_database_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to restore CMEK database '{new_database_id}' "
            f"from backup '{backup_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        key_id = restored.encryption_config.kms_key_name.split("/")[-1]
        print(f"Resource ID: {new_database_id}")
        print(f"Encryption Key ID: {key_id}")
        print(f"Restored From Backup: {backup_id}")


# [END spanner_restore_backup_with_encryption_key]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Restore a Spanner backup into a CMEK-encrypted database."
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
        "--new-database-id",
        default="example-restored-cmek-db",
    )
    parser.add_argument(
        "--backup-id",
        default=os.environ.get("SPANNER_BACKUP_ID", "example-backup"),
    )
    parser.add_argument(
        "--kms-key-name",
        default=os.environ.get(
            "SPANNER_KMS_KEY_NAME",
            "projects/example-project-id/locations/us-central1/keyRings/example-ring/cryptoKeys/example-key",
        ),
    )
    args = parser.parse_args()

    restore_backup_with_encryption_key(
        project_id=args.project_id,
        instance_id=args.instance_id,
        new_database_id=args.new_database_id,
        backup_id=args.backup_id,
        kms_key_name=args.kms_key_name,
    )
