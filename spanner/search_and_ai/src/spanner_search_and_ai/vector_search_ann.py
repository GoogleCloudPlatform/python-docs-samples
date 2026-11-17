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

# [START spanner_vector_search_ann]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def find_approximate_nearest_neighbors(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Finds approximate nearest neighbors using a ScaNN vector index.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Enterprise-edition Spanner instance ID.
        database_id: The Spanner database ID containing CatalogItems and
            CatalogEmbeddingIndex.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)

    query_embedding = [0.8, 0.5, 0.2, 0.15]
    sql = """
        SELECT ItemId, Title,
               APPROX_COSINE_DISTANCE(
                   @query_vector,
                   Embedding,
                   options => JSON '{"num_leaves_to_search": 10}'
               ) AS approx_distance
        FROM CatalogItems@{FORCE_INDEX=CatalogEmbeddingIndex}
        WHERE WordCount > @min_words AND Embedding IS NOT NULL
        ORDER BY approx_distance
        LIMIT @top_k
    """
    params = {
        "query_vector": query_embedding,
        "min_words": 1000,
        "top_k": 3,
    }
    query_param_types = {
        "query_vector": param_types.Array(param_types.FLOAT32),
        "min_words": param_types.INT64,
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
            f"error: ANN vector search failed on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for item_id, title, approx_distance in rows:
            print(f"Approx Distance: {approx_distance:.6f}")
            print(f"Item ID: {item_id}")
            print(f"Title: {title}")


# [END spanner_vector_search_ann]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run an approximate nearest neighbor (ANN) search in Spanner."
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

    find_approximate_nearest_neighbors(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
