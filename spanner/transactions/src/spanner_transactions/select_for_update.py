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

# [START spanner_select_for_update]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1
from google.cloud.spanner_v1 import param_types


def transfer_budget_with_select_for_update(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Validates read ranges with SELECT FOR UPDATE in repeatable read isolation.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Albums table.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    transfer_amount = 10000
    updated_budgets: dict[str, int] = {}

    def update_albums(transaction: spanner_v1.Transaction) -> None:
        # FOR UPDATE validates at commit time that the read cells were not
        # concurrently modified under REPEATABLE_READ isolation.
        select_sql = """
            SELECT MarketingBudget
            FROM Albums
            WHERE SingerId = @singer_id AND AlbumId = @album_id
            FOR UPDATE
        """
        source_rows = list(
            transaction.execute_sql(
                select_sql,
                params={"singer_id": 2, "album_id": 2},
                param_types={
                    "singer_id": param_types.INT64,
                    "album_id": param_types.INT64,
                },
            )
        )
        target_rows = list(
            transaction.execute_sql(
                select_sql,
                params={"singer_id": 1, "album_id": 1},
                param_types={
                    "singer_id": param_types.INT64,
                    "album_id": param_types.INT64,
                },
            )
        )
        if not source_rows or not target_rows:
            raise ValueError("Source or target album row was not found.")
        source_budget = int(source_rows[0][0] or 0) - transfer_amount
        target_budget = int(target_rows[0][0] or 0) + transfer_amount

        update_sql = """
            UPDATE Albums
            SET MarketingBudget = @budget
            WHERE SingerId = @singer_id AND AlbumId = @album_id
        """
        update_types = {
            "budget": param_types.INT64,
            "singer_id": param_types.INT64,
            "album_id": param_types.INT64,
        }
        transaction.execute_update(
            update_sql,
            params={"budget": source_budget, "singer_id": 2, "album_id": 2},
            param_types=update_types,
        )
        transaction.execute_update(
            update_sql,
            params={"budget": target_budget, "singer_id": 1, "album_id": 1},
            param_types=update_types,
        )
        updated_budgets["source"] = source_budget
        updated_budgets["target"] = target_budget

    try:
        database.run_in_transaction(
            update_albums,
            isolation_level=spanner_v1.TransactionOptions.IsolationLevel.REPEATABLE_READ,
        )
    except ValueError as err:
        print(
            f"error: cannot transfer budget on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err}",
            file=sys.stderr,
        )
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"in project '{project_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: SELECT FOR UPDATE transaction failed on database "
            f"'{database_id}' in instance '{instance_id}' for project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        print("Isolation Level: REPEATABLE_READ")
        print(f"Source Budget: {updated_budgets['source']}")
        print(f"Target Budget: {updated_budgets['target']}")


# [END spanner_select_for_update]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run SELECT FOR UPDATE inside a repeatable-read transaction."
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

    transfer_budget_with_select_for_update(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
