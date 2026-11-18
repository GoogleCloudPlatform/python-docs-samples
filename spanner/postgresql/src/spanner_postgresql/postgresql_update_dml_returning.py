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

# [START spanner_postgresql_update_dml_returning]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def postgresql_update_dml_returning(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Updates Albums MarketingBudget in PostgreSQL Spanner with RETURNING.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The PostgreSQL-dialect Spanner database ID.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    budgets: list[int] = []
    row_count = 0

    def update_albums(transaction: spanner_v1.Transaction) -> None:
        nonlocal row_count
        budgets.clear()
        results = transaction.execute_sql(
            "UPDATE Albums "
            "SET MarketingBudget = MarketingBudget * 2 "
            "WHERE SingerId = 1 AND AlbumId = 1 "
            "RETURNING MarketingBudget"
        )
        for row in results:
            budgets.append(int(row[0] or 0))
        row_count = int(results.stats.row_count_exact) if results.stats else 0

    try:
        database.run_in_transaction(update_albums)
    except exceptions.NotFound as err:
        print(
            f"error: PostgreSQL database '{database_id}' on instance "
            f"'{instance_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: PostgreSQL UPDATE RETURNING failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        for budget in budgets:
            print(f"Marketing Budget: {budget}")
        print(f"Updated Rows: {row_count}")


# [END spanner_postgresql_update_dml_returning]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Update Albums rows using PostgreSQL-dialect DML RETURNING."
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
        default=os.environ.get("SPANNER_DATABASE_ID", "example-pg-db"),
        help="PostgreSQL-dialect Spanner database ID (default: $SPANNER_DATABASE_ID)",
    )
    args = parser.parse_args()

    postgresql_update_dml_returning(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
