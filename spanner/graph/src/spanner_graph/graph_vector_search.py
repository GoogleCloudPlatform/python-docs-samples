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

# [START spanner_graph_vector_search]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def run_graph_vector_search(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Finds K-nearest neighbor accounts in Spanner Graph via GQL and vectors.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Enterprise-edition Spanner instance ID.
        database_id: The Spanner database ID containing the FinGraph schema.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)

    sql = """
        GRAPH FinGraph
        MATCH (p:Person)-[:Owns]->(a:Account)
        WHERE a.nick_name_embeddings IS NOT NULL
        RETURN p.name AS owner_name,
               a.nick_name AS account_nickname,
               EUCLIDEAN_DISTANCE(a.nick_name_embeddings, @query_vector) AS distance
        ORDER BY distance
        LIMIT @top_k
    """
    params = {
        "query_vector": [0.2, 0.4, 0.9, 0.6],
        "top_k": 2,
    }
    query_param_types = {
        "query_vector": param_types.Array(param_types.FLOAT32),
        "top_k": param_types.INT64,
    }

    try:
        with database.snapshot() as snapshot:
            rows = list(
                snapshot.execute_sql(
                    sql,
                    params=params,
                    param_types=query_param_types,
                )
            )
    except exceptions.NotFound as err:
        print(
            f"error: database '{database_id}' on instance '{instance_id}' "
            f"in project '{project_id}' was not found: {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: graph vector search failed on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for owner_name, account_nickname, distance in rows:
            print(f"Account Nickname: {account_nickname}")
            print(f"Distance: {distance:.6f}")
            print(f"Owner Name: {owner_name}")


# [END spanner_graph_vector_search]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run KNN vector similarity search on Spanner Graph nodes."
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

    run_graph_vector_search(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
