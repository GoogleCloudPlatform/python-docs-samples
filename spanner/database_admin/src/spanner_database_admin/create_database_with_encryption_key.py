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

# [START spanner_create_database_with_encryption_key]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_database_with_encryption_key(
    project_id: str, instance_id: str, database_id: str, kms_key_name: str
) -> None:
    """Creates a Spanner database protected by a single-region Cloud KMS key.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The new Spanner database ID to create.
        kms_key_name: The Cloud KMS CryptoKey resource path.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    parent = client.instance_path(project_id, instance_id)
    encryption_config = spanner_admin_database_v1.EncryptionConfig(
        kms_key_name=kms_key_name
    )
    request = spanner_admin_database_v1.CreateDatabaseRequest(
        parent=parent,
        create_statement=f"CREATE DATABASE `{database_id}`",
        extra_statements=[
            "CREATE TABLE Singers ("
            "  SingerId INT64 NOT NULL,"
            "  FirstName STRING(1024),"
            "  LastName STRING(1024)"
            ") PRIMARY KEY (SingerId)",
        ],
        encryption_config=encryption_config,
    )

    try:
        operation = client.create_database(request=request)
        print(f"Waiting for CMEK database '{database_id}' creation...")
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
            f"error: failed to create CMEK database '{database_id}' on "
            f"instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        configured_key_id = database.encryption_config.kms_key_name.split("/")[-1]
        print(f"Resource ID: {database_id}")
        print(f"Encryption Key ID: {configured_key_id}")


# [END spanner_create_database_with_encryption_key]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Create a Spanner database encrypted with Cloud KMS CMEK."
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
        default=os.environ.get("SPANNER_DATABASE_ID", "example-cmek-db"),
    )
    parser.add_argument(
        "--kms-key-name",
        default=os.environ.get(
            "SPANNER_KMS_KEY_NAME",
            "projects/example-project-id/locations/us-central1/keyRings/example-ring/cryptoKeys/example-key",
        ),
    )
    args = parser.parse_args()

    create_database_with_encryption_key(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
        kms_key_name=args.kms_key_name,
    )
