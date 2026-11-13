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

# [START bigquery_vector_search]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def vector_search(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Runs an indexed vector similarity search using a parameterized embedding array.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the embeddings table
            (for example, 'example_dataset').
        table_id: BigQuery table ID containing the indexed embedding column
            (for example, 'example_embeddings').
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # Pass the query embedding via ArrayQueryParameter and specify fraction_lists_to_search
    # to control the recall-latency tradeoff across indexed inverted lists.
    query_embedding = [1.0, 0.5, 0.25, 0.125]
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("query_embedding", "FLOAT64", query_embedding),
        ]
    )
    sql = f"""
        SELECT
          base.id AS matched_id,
          distance
        FROM VECTOR_SEARCH(
          TABLE `{table_ref}`,
          'embedding',
          (SELECT @query_embedding AS query_embedding),
          query_column_to_search => 'query_embedding',
          top_k => 3,
          distance_type => 'COSINE',
          options => '{{"fraction_lists_to_search": 0.05}}'
        )
        ORDER BY distance ASC, matched_id ASC;
    """

    try:
        print(f"Running indexed vector similarity search on table: {table_ref}")
        query_job = client.query(sql, job_config=job_config)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: embeddings table '{table_id}' not found in dataset '{dataset_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to run vector search on table '{table_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print("Distance Type: COSINE")
    print(f"Embedding Dimensions: {len(query_embedding)}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Neighbors Returned: {len(rows)}")


# [END bigquery_vector_search]
