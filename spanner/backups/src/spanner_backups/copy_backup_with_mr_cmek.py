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

# [START spanner_copy_backup_with_mr_cmek]
import datetime
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def copy_backup_with_mr_cmek(
    project_id: str,
    destination_instance_id: str,
    destination_backup_id: str,
    source_instance_id: str,
    source_backup_id: str,
    kms_key_names: list[str],
) -> None:
    """Copies a Spanner backup into a multi-region CMEK destination backup.

    Args:
        project_id: The Google Cloud project ID.
        destination_instance_id: The multi-region destination instance ID.
        destination_backup_id: The new destination backup ID.
        source_instance_id: The source Spanner instance ID.
        source_backup_id: The source backup ID to copy.
        kms_key_names: Regional Cloud KMS CryptoKey resource paths.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, destination_instance_id)
    source_backup = client.backup_path(project_id, source_instance_id, source_backup_id)
    expire_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=7
    )
    enc_type = (
        spanner_admin_database_v1.CopyBackupEncryptionConfig.EncryptionType.CUSTOMER_MANAGED_ENCRYPTION
    )
    encryption_config = spanner_admin_database_v1.CopyBackupEncryptionConfig(
        encryption_type=enc_type,
        kms_key_names=kms_key_names,
    )
    request = spanner_admin_database_v1.CopyBackupRequest(
        parent=parent,
        backup_id=destination_backup_id,
        source_backup=source_backup,
        expire_time=expire_time,
        encryption_config=encryption_config,
    )

    try:
        operation = client.copy_backup(request=request)
        print(
            f"Waiting for multi-region CMEK copy '{destination_backup_id}' "
            f"from '{source_backup_id}'..."
        )
        copied = operation.result(timeout=2100)
    except exceptions.AlreadyExists as err:
        print(
            f"error: destination backup '{destination_backup_id}' already "
            f"exists on instance '{destination_instance_id}': {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on "
            f"destination backup '{destination_backup_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to copy backup '{source_backup_id}' to "
            f"'{destination_backup_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        enc_count = len(copied.encryption_information)
        print(f"Resource ID: {destination_backup_id}")
        print(f"Backup Size Bytes: {copied.size_bytes}")
        print(f"Encryption Info Entries: {enc_count}")


# [END spanner_copy_backup_with_mr_cmek]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Copy a Spanner backup using multi-region CMEK keys."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--destination-instance-id",
        default=os.environ.get("SPANNER_MR_INSTANCE_ID", "example-mr-instance"),
    )
    parser.add_argument(
        "--destination-backup-id",
        default="example-copied-mr-backup",
    )
    parser.add_argument(
        "--source-instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
    )
    parser.add_argument(
        "--source-backup-id",
        default=os.environ.get("SPANNER_BACKUP_ID", "example-source-backup"),
    )
    parser.add_argument(
        "--kms-key-names",
        default=os.environ.get(
            "SPANNER_MR_KMS_KEY_NAMES",
            "projects/example-project-id/locations/us-central1/keyRings/example-ring/cryptoKeys/example-key,"
            "projects/example-project-id/locations/us-east1/keyRings/example-ring/cryptoKeys/example-key,"
            "projects/example-project-id/locations/us-east4/keyRings/example-ring/cryptoKeys/example-key",
        ),
    )
    args = parser.parse_args()

    copy_backup_with_mr_cmek(
        project_id=args.project_id,
        destination_instance_id=args.destination_instance_id,
        destination_backup_id=args.destination_backup_id,
        source_instance_id=args.source_instance_id,
        source_backup_id=args.source_backup_id,
        kms_key_names=[k.strip() for k in args.kms_key_names.split(",") if k.strip()],
    )
