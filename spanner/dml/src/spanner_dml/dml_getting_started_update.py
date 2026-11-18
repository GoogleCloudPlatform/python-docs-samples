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

# [START spanner_dml_getting_started_update]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1
from google.cloud.spanner_v1 import param_types


def transfer_budget_with_dml(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Atomically transfers MarketingBudget between two albums using DML.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Albums.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    transfer_amount = 200000
    budget_types = {"AlbumBudget": param_types.INT64}
    updated_first_budget = 0
    updated_second_budget = 0
    updated_rows = 0

    def transfer_budget(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal updated_first_budget, updated_second_budget, updated_rows
        second_row = next(
            iter(
                transaction.execute_sql(
                    "SELECT MarketingBudget FROM Albums "
                    "WHERE SingerId = 2 AND AlbumId = 2"
                )
            )
        )
        second_budget = int(second_row[0] or 0)
        if second_budget < transfer_amount:
            return

        first_row = next(
            iter(
                transaction.execute_sql(
                    "SELECT MarketingBudget FROM Albums "
                    "WHERE SingerId = 1 AND AlbumId = 1"
                )
            )
        )
        updated_first_budget = int(first_row[0] or 0) + transfer_amount
        updated_second_budget = second_budget - transfer_amount

        first_params = {"AlbumBudget": updated_first_budget}
        second_params = {"AlbumBudget": updated_second_budget}
        first_ct = transaction.execute_update(
            "UPDATE Albums SET MarketingBudget = @AlbumBudget "
            "WHERE SingerId = 1 AND AlbumId = 1",
            params=first_params,
            param_types=budget_types,
        )
        second_ct = transaction.execute_update(
            "UPDATE Albums SET MarketingBudget = @AlbumBudget "
            "WHERE SingerId = 2 AND AlbumId = 2",
            params=second_params,
            param_types=budget_types,
        )
        updated_rows = first_ct + second_ct

    try:
        database.run_in_transaction(transfer_budget)
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: DML budget transfer failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"First Album Budget: {updated_first_budget}")
        print(f"Second Album Budget: {updated_second_budget}")
        print(f"Updated Rows: {updated_rows}")


# [END spanner_dml_getting_started_update]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Transfer MarketingBudget between two albums in a DML transaction."
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

    transfer_budget_with_dml(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
