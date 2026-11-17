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

# [START spanner_hybrid_search_rrf]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def run_hybrid_search_rrf(project_id: str, instance_id: str, database_id: str) -> None:
    """Combines full-text and ANN vector search via Reciprocal Rank Fusion.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Enterprise-edition Spanner instance ID.
        database_id: The Spanner database ID containing CatalogItems,
            CatalogEmbeddingIndex, and CatalogSearchIndex.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)

    # Reciprocal Rank Fusion (RRF) merges incompatible distance and text scores
    # by summing 1 / (k + rank) across both retrievers on the server.
    sql = """
        SELECT rrf.ItemId, items.Title, rrf.rrf_score
        FROM (
            SELECT ItemId, SUM(1.0 / (60 + rank)) AS rrf_score
            FROM (
                (
                    SELECT x AS ItemId, rank
                    FROM UNNEST(ARRAY(
                        SELECT ItemId
                        FROM CatalogItems@{FORCE_INDEX=CatalogEmbeddingIndex}
                        ORDER BY APPROX_COSINE_DISTANCE(
                            @query_vector,
                            Embedding,
                            options => JSON '{"num_leaves_to_search": 10}'
                        )
                        LIMIT 20
                    )) AS x WITH OFFSET AS rank
                )
                UNION ALL
                (
                    SELECT x AS ItemId, rank
                    FROM UNNEST(ARRAY(
                        SELECT ItemId
                        FROM CatalogItems@{FORCE_INDEX=CatalogSearchIndex}
                        WHERE SEARCH(Description_Tokens, @search_query)
                        ORDER BY SCORE(Description_Tokens, @search_query) DESC
                        LIMIT 20
                    )) AS x WITH OFFSET AS rank
                )
            )
            GROUP BY ItemId
        ) AS rrf
        JOIN CatalogItems AS items ON rrf.ItemId = items.ItemId
        ORDER BY rrf.rrf_score DESC, rrf.ItemId ASC
        LIMIT @top_k
    """
    params = {
        "query_vector": [0.8, 0.5, 0.2, 0.15],
        "search_query": "waterproof alpine",
        "top_k": 5,
    }
    query_param_types = {
        "query_vector": param_types.Array(param_types.FLOAT32),
        "search_query": param_types.STRING,
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
            f"error: hybrid RRF search failed on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for item_id, title, rrf_score in rows:
            print(f"Item ID: {item_id}")
            print(f"RRF Score: {rrf_score:.6f}")
            print(f"Title: {title}")


# [END spanner_hybrid_search_rrf]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run a hybrid full-text and vector RRF search in Spanner."
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

    run_hybrid_search_rrf(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
