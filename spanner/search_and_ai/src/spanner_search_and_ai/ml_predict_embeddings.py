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

# [START spanner_ml_predict_embeddings]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def generate_and_query_embeddings(
    project_id: str, instance_id: str, database_id: str
) -> None:
    """Generates text embeddings via ML.PREDICT and ranks products by distance.

    Generating embeddings in a read-only snapshot avoids holding read-write
    locks during remote Vertex AI inference calls.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID with TextEmbeddingModel and
            Products registered.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)

    sql = """
        WITH product_vectors AS (
            SELECT ProductId, Name, embeddings.values AS doc_vector
            FROM ML.PREDICT(
                MODEL TextEmbeddingModel,
                (
                    SELECT ProductId, Name, Description AS content,
                           'RETRIEVAL_DOCUMENT' AS task_type
                    FROM Products
                ),
                STRUCT(768 AS outputDimensionality)
            )
        ),
        query_vector AS (
            SELECT embeddings.values AS user_vector
            FROM ML.PREDICT(
                MODEL TextEmbeddingModel,
                (
                    SELECT @search_text AS content,
                           'RETRIEVAL_QUERY' AS task_type
                ),
                STRUCT(768 AS outputDimensionality)
            )
        )
        SELECT p.ProductId, p.Name,
               COSINE_DISTANCE(p.doc_vector, q.user_vector) AS distance
        FROM product_vectors AS p
        CROSS JOIN query_vector AS q
        ORDER BY distance
        LIMIT @top_k
    """
    params = {
        "search_text": "home repair power tool",
        "top_k": 3,
    }
    query_param_types = {
        "search_text": param_types.STRING,
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
            f"error: database '{database_id}' or model on instance "
            f"'{instance_id}' in project '{project_id}' was not found: "
            f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: ML.PREDICT embedding query failed on database "
            f"'{database_id}' in instance '{instance_id}' for project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for product_id, name, distance in rows:
            print(f"Cosine Distance: {distance:.6f}")
            print(f"Product ID: {product_id}")
            print(f"Product Name: {name}")


# [END spanner_ml_predict_embeddings]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate and compare text embeddings via Spanner ML.PREDICT."
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

    generate_and_query_embeddings(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
