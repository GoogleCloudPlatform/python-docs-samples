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

# [START spanner_vector_search_knn]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def find_k_nearest_neighbors(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Finds exact K-nearest neighbors using COSINE_DISTANCE and FLOAT32 vectors.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing the Documents table.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)

    # Bind the query vector as ARRAY<FLOAT32> to match the vector_length=>4 column.
    query_embedding = [0.3, 0.3, 0.7, 0.7]
    sql = """
        SELECT DocId, Title,
               COSINE_DISTANCE(DocEmbedding, @query_vector) AS distance
        FROM Documents
        WHERE UserId = @user_id
        ORDER BY distance
        LIMIT @top_k
    """
    params = {
        "query_vector": query_embedding,
        "user_id": 1,
        "top_k": 3,
    }
    query_param_types = {
        "query_vector": param_types.Array(param_types.FLOAT32),
        "user_id": param_types.INT64,
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
            f"error: KNN vector search failed on database '{database_id}' "
            f"in instance '{instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for doc_id, title, distance in rows:
            print(f"Distance: {distance:.6f}")
            print(f"Document ID: {doc_id}")
            print(f"Title: {title}")


# [END spanner_vector_search_knn]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Run an exact KNN vector similarity search in Spanner."
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

    find_k_nearest_neighbors(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
