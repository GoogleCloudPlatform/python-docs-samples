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

# [START spanner_dml_standard_delete]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def delete_data_with_dml(project_id: str, instance_id: str, database_id: str) -> None:
    """Deletes Singers rows matching a predicate using GoogleSQL DML.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Singers.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    deleted_rows = 0

    def delete_singers(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal deleted_rows
        deleted_rows = transaction.execute_update(
            "DELETE FROM Singers WHERE FirstName = 'Alice'"
        )

    try:
        database.run_in_transaction(delete_singers)
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: DML delete failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Deleted Rows: {deleted_rows}")


# [END spanner_dml_standard_delete]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Delete Singers rows using GoogleSQL DML."
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
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
        help="Spanner database ID (default: $SPANNER_DATABASE_ID)",
    )
    args = parser.parse_args()

    delete_data_with_dml(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
