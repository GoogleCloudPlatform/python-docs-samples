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

# [START spanner_create_backup_with_encryption_key]
import datetime
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_backup_with_encryption_key(
    project_id: str,
    instance_id: str,
    database_id: str,
    backup_id: str,
    kms_key_name: str,
) -> None:
    """Creates a Spanner database backup protected by a Cloud KMS CMEK key.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The source Spanner database ID.
        backup_id: The new backup ID to create.
        kms_key_name: The Cloud KMS CryptoKey resource path.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    database_path = client.database_path(project_id, instance_id, database_id)
    expire_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=7
    )
    enc_type = (
        spanner_admin_database_v1.CreateBackupEncryptionConfig.EncryptionType.CUSTOMER_MANAGED_ENCRYPTION
    )
    encryption_config = spanner_admin_database_v1.CreateBackupEncryptionConfig(
        encryption_type=enc_type,
        kms_key_name=kms_key_name,
    )
    backup_pb = spanner_admin_database_v1.Backup(
        database=database_path,
        expire_time=expire_time,
    )
    request = spanner_admin_database_v1.CreateBackupRequest(
        parent=parent,
        backup_id=backup_id,
        backup=backup_pb,
        encryption_config=encryption_config,
    )

    try:
        operation = client.create_backup(request=request)
        print(f"Waiting for CMEK backup '{backup_id}' creation...")
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
            f"error: failed to create CMEK backup '{backup_id}' on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        enc_state = backup.encryption_info.encryption_type.name
        print(f"Resource ID: {backup_id}")
        print(f"Backup Size Bytes: {backup.size_bytes}")
        print(f"Encryption Type: {enc_state}")


# [END spanner_create_backup_with_encryption_key]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a CMEK-encrypted Spanner database backup."
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
        default="example-cmek-backup",
    )
    parser.add_argument(
        "--kms-key-name",
        default=os.environ.get(
            "SPANNER_KMS_KEY_NAME",
            "projects/example-project-id/locations/us-central1/keyRings/example-ring/cryptoKeys/example-key",
        ),
    )
    args = parser.parse_args()

    create_backup_with_encryption_key(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        backup_id=args.backup_id,
        kms_key_name=args.kms_key_name,
    )
