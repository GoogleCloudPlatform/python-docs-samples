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

# [START bigquery_create_vector_index_tree_ah]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def create_vector_index_tree_ah(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Creates a TreeAH vector index on an embedding column in a BigQuery table.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the target table
            (for example, 'example_dataset').
        table_id: BigQuery table ID containing the embedding column
            (for example, 'example_embeddings').
    """
    client = bigquery.Client(project=project_id)
    index_name = "example_tree_ah_index"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # TreeAH indexes use asymmetric hashing optimized for batch and single-query vector search.
    sql = f"""
        CREATE OR REPLACE VECTOR INDEX `{index_name}`
        ON `{table_ref}`(embedding)
        OPTIONS(
          index_type = 'TREE_AH',
          distance_type = 'COSINE',
          tree_ah_options = '{{"normalization_type": "L2"}}'
        );
    """

    try:
        print(f"Creating TreeAH vector index {index_name} on table: {table_ref}")
        query_job = client.query(sql)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: table '{table_id}' or dataset '{dataset_id}' not found in "
            f"project '{project_id}' when creating index '{index_name}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create TreeAH vector index '{index_name}' on table "
            f"'{table_id}' in dataset '{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Index Name: {index_name}")
    print("Index Type: TREE_AH")
    print(f"Job ID: {query_job.job_id}")
    print(f"Statement Type: {query_job.statement_type}")


# [END bigquery_create_vector_index_tree_ah]
