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

# [START spanner_graph_full_text_search]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def run_graph_full_text_search(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Combines full-text SEARCH() and SCORE() with GQL graph traversal.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Enterprise-edition Spanner instance ID.
        database_id: The Spanner database ID containing FinGraph and
            AccountTextSearchIndex.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)

    sql = """
        GRAPH FinGraph
        MATCH (n:Account)<-[e:Transfers]-(:Account)
        WHERE SEARCH(n.nick_name_token, @search_query)
        RETURN n.nick_name,
               e.amount AS amount_added,
               SCORE(n.nick_name_token, @search_query) AS relevance_score
        ORDER BY relevance_score DESC
    """
    params = {"search_query": '"rainy day" | vacation'}
    query_param_types = {"search_query": param_types.STRING}

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
            f"error: graph full-text search failed on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for nick_name, amount_added, relevance_score in rows:
            print(f"Account Nickname: {nick_name}")
            print(f"Amount Added: {amount_added:.2f}")
            print(f"Relevance Score: {relevance_score:.6f}")


# [END spanner_graph_full_text_search]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run full-text search combined with GQL traversal in Spanner Graph."
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

    run_graph_full_text_search(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
