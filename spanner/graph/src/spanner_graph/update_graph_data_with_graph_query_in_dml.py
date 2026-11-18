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

# [START spanner_update_graph_data_with_graph_query_in_dml]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_v1


def update_graph_data_with_graph_query_in_dml(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Updates Account nodes matched by an embedded GQL path subquery in DML.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing FinGraph.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    updated_accounts = 0

    def update_accounts(transaction: spanner_v1.transaction.Transaction) -> None:
        nonlocal updated_accounts
        updated_accounts = transaction.execute_update(
            "UPDATE Account SET is_blocked = true "
            "WHERE id IN {"
            "  GRAPH FinGraph "
            "  MATCH (a:Account WHERE a.id = 1)-[:Transfers]->{1,2}(b:Account) "
            "  RETURN b.id"
            "}"
        )

    try:
        database.run_in_transaction(update_accounts)
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: DML update with embedded GQL query failed on database "
            f"'{database_id}' in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Updated Accounts: {updated_accounts}")


# [END spanner_update_graph_data_with_graph_query_in_dml]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Update Account rows matched by an embedded GQL subquery in DML."
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
        help="Spanner database ID",
    )
    args = parser.parse_args()

    update_graph_data_with_graph_query_in_dml(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
