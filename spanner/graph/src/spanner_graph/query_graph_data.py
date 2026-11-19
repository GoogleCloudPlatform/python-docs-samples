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

# [START spanner_query_graph_data]
import sys

from google.api_core import exceptions
from google.cloud import spanner


def query_graph_data(project_id: str, instance_id: str, database_id: str) -> None:
    """Executes a multi-hop GQL MATCH query over FinGraph in a read snapshot.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing FinGraph.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    gql = """
        GRAPH FinGraph
        MATCH (a:Person)-[o:Owns]->()-[t:Transfers]->()<-[p:Owns]-(b:Person)
        RETURN a.name AS sender, b.name AS receiver,
               t.amount, t.create_time AS transfer_at
    """

    try:
        with database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(gql))
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: GQL query failed on database '{database_id}' "
            f"in instance '{instance_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Matched Transfers: {len(rows)}")
        for sender, receiver, amount, transfer_at in rows:
            print(
                f"Transfer Sender: {sender}, Receiver: {receiver}, "
                f"Amount: {amount}, At: {transfer_at}"
            )


# [END spanner_query_graph_data]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run a GQL multi-hop pattern match query on FinGraph."
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

    query_graph_data(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
