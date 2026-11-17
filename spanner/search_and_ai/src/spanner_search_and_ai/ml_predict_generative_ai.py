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

# [START spanner_ml_predict_generative_ai]
import sys

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


def generate_product_recommendations(
    project_id: str,
    instance_id: str,
    database_id: str,
) -> None:
    """Registers a remote Gemini model and evaluates product recommendations.

    Args:
        project_id: The Google Cloud project ID.
        instance_id: The Spanner instance ID.
        database_id: The Spanner database ID containing Products, Categories,
            and Users.
    """
    client = spanner.Client(project=project_id)
    database = client.instance(instance_id).database(database_id)
    location = "global"
    model_name = "GeminiRecommendationModel"
    endpoint = (
        f"//aiplatform.googleapis.com/projects/{project_id}"
        f"/locations/{location}/publishers/google/models/gemini-3.8-flash"
    )
    ddl_statement = f"""
        CREATE OR REPLACE MODEL {model_name}
        INPUT (prompt STRING(MAX))
        OUTPUT (content STRING(MAX))
        REMOTE OPTIONS (
            endpoint = '{endpoint}',
            default_batch_size = 1
        )
    """.strip()

    # Reserve enough maxOutputTokens for Gemini thinking tokens before text output.
    sql = f"""
        SELECT ProductId, Name, TRIM(content) AS recommendation
        FROM ML.PREDICT(
            MODEL {model_name},
            (
                SELECT product.ProductId,
                       product.Name,
                       CONCAT(
                           'Answer YES or NO only: Is this product a good fit? ',
                           'Age: ', CAST(customer.Age AS STRING), '; ',
                           'Interests: ', customer.Likes, '; ',
                           'Product: ', product.Name, ' (', category.Name, ') - ',
                           product.Description
                       ) AS prompt
                FROM Products AS product
                JOIN Categories AS category
                    ON product.CategoryId = category.CategoryId
                JOIN Users AS customer
                    ON customer.UserId = @user_id
            ),
            STRUCT(1024 AS maxOutputTokens, 0.0 AS temperature)
        )
        ORDER BY ProductId
    """
    params = {"user_id": 1}
    query_param_types = {"user_id": param_types.INT64}

    try:
        print(f"Waiting for remote Gemini model '{model_name}' registration...")
        database.update_ddl([ddl_statement]).result(timeout=300)
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
            f"error: database '{database_id}' or Vertex AI model on instance "
            f"'{instance_id}' for project '{project_id}' was not found: "
            f"{err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: Gemini ML.PREDICT recommendation query failed on database "
            f"'{database_id}' in instance '{instance_id}' for project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database.name}")
        for product_id, name, recommendation in rows:
            print(f"Product ID: {product_id}")
            print(f"Product Name: {name}")
            print(f"Recommendation: {recommendation}")


# [END spanner_ml_predict_generative_ai]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Evaluate product recommendations with Gemini via Spanner ML.PREDICT."
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

    generate_product_recommendations(
        project_id=args.project_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
