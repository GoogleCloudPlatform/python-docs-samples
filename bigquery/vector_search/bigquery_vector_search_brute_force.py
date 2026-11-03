# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bigquery_vector_search_brute_force]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def vector_search_brute_force(
    project_id: str,
) -> None:
    """Runs an exact brute-force vector similarity search over BBC news embeddings.

    Args:
        project_id: Google Cloud project ID used to bill the query job
            (for example, 'example-project').
    """
    client = bigquery.Client(project=project_id)
    # Query the public BBC News dataset in bigquery-public-data
    # (https://cloud.google.com/bigquery/public-data).
    table_ref = "bigquery-public-data.bbc_news.fulltext"
    # Pass a 768-dimensional query vector and enable use_brute_force for exact distance calculation.
    category_filter = "tech"
    query_embedding = [0.01] * 768
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("category_filter", "STRING", category_filter),
            bigquery.ArrayQueryParameter("query_embedding", "FLOAT64", query_embedding),
        ]
    )
    sql = f"""
        SELECT
          base.title AS matched_title,
          base.category AS matched_category,
          distance
        FROM VECTOR_SEARCH(
          (
            SELECT
              title,
              category,
              body_embedded
            FROM `{table_ref}`
            WHERE category = @category_filter
              AND ARRAY_LENGTH(body_embedded) = 768
          ),
          'body_embedded',
          (SELECT @query_embedding AS query_embedding),
          query_column_to_search => 'query_embedding',
          top_k => 5,
          distance_type => 'COSINE',
          options => '{{"use_brute_force": true}}'
        )
        ORDER BY distance ASC, matched_title ASC;
    """

    try:
        print(
            f"Running brute-force vector search on {table_ref} (category={category_filter})"
        )
        query_job = client.query(sql, job_config=job_config)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: public embeddings table '{table_ref}' not found when querying "
            f"from project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to run brute-force vector search on '{table_ref}' in "
            f"project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print("Distance Type: COSINE")
    print(f"Embedding Dimensions: {len(query_embedding)}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Neighbors Returned: {len(rows)}")


# [END bigquery_vector_search_brute_force]
