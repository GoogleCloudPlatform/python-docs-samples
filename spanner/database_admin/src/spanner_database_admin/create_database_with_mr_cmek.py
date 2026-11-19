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

# [START spanner_create_database_with_mr_cmek]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_database_with_mr_cmek(
    project_id: str,
    instance_id: str,
    database_id: str,
    kms_key_names: list[str],
) -> None:
    """Creates a multi-region Spanner database protected by regional KMS keys.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The multi-region Spanner instance ID.
        database_id: The new Spanner database ID to create.
        kms_key_names: Regional Cloud KMS CryptoKey resource paths.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    encryption_config = spanner_admin_database_v1.EncryptionConfig(
        kms_key_names=kms_key_names
    )
    request = spanner_admin_database_v1.CreateDatabaseRequest(
        parent=parent,
        create_statement=f"CREATE DATABASE `{database_id}`",
        extra_statements=[
            """
            CREATE TABLE Singers (
              SingerId INT64 NOT NULL,
              FirstName STRING(1024),
              LastName STRING(1024)
            ) PRIMARY KEY (SingerId)
            """,
        ],
        encryption_config=encryption_config,
    )

    try:
        operation = client.create_database(request=request)
        print(f"Waiting for multi-region CMEK database '{database_id}' creation...")
        database = operation.result(timeout=300)
    except exceptions.AlreadyExists as err:
        print(
            f"error: database '{database_id}' already exists on instance "
            f"'{instance_id}': {err.message}",
            file=sys.stderr,
        )
    except TimeoutError as err:
        print(
            f"error: timed out waiting for the operation on database '{database_id}' "
            f"to complete; the operation may still be running: {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create multi-region CMEK database '{database_id}' "
            f"on instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        key_count = len(database.encryption_config.kms_key_names)
        print(f"Resource ID: {database_id}")
        print(f"Configured KMS Keys: {key_count}")


# [END spanner_create_database_with_mr_cmek]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a multi-region Spanner database with regional KMS keys."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_MR_INSTANCE_ID", "example-mr-instance"),
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-mr-cmek-db"),
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

    create_database_with_mr_cmek(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        kms_key_names=[k.strip() for k in args.kms_key_names.split(",") if k.strip()],
    )
