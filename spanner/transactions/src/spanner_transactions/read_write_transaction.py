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

# [START spanner_read_write_transaction]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def read_write_transaction(project_id: str, instance_id: str, database_id: str) -> None:
    """Transfers MarketingBudget atomically inside a read-write transaction.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Albums.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    first_key = spanner.KeySet(keys=[[1, 1]])
    second_key = spanner.KeySet(keys=[[2, 2]])
    budget_cols = ("MarketingBudget",)
    update_cols = ("SingerId", "AlbumId", "MarketingBudget")
    transfer_amount = 200000
    updated_first_budget = 0
    updated_second_budget = 0

    def update_albums(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal updated_first_budget, updated_second_budget
        second_row = next(
            iter(
                transaction.read(
                    table="Albums",
                    columns=budget_cols,
                    keyset=second_key,
                    limit=1,
                )
            )
        )
        second_budget = int(second_row[0] or 0)
        if second_budget < transfer_amount:
            raise ValueError("Second album does not have sufficient funds.")

        first_row = next(
            iter(
                transaction.read(
                    table="Albums",
                    columns=budget_cols,
                    keyset=first_key,
                    limit=1,
                )
            )
        )
        updated_first_budget = int(first_row[0] or 0) + transfer_amount
        updated_second_budget = second_budget - transfer_amount
        updated_values = [
            (1, 1, updated_first_budget),
            (2, 2, updated_second_budget),
        ]
        transaction.update(table="Albums", columns=update_cols, values=updated_values)

    try:
        database.run_in_transaction(update_albums)
    except ValueError as err:
        print(
            f"error: read-write transaction aborted due to business rule on "
            f"database '{database_id}': {err}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: read-write transaction failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"First Album Budget: {updated_first_budget}")
        print(f"Second Album Budget: {updated_second_budget}")


# [END spanner_read_write_transaction]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Transfer MarketingBudget inside a read-write transaction."
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

    read_write_transaction(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
