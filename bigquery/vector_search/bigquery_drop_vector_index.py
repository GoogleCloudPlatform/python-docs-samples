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

# [START bigquery_drop_vector_index]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def drop_vector_index(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Drops a vector index from a BigQuery embeddings table.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the indexed table
            (for example, 'example_dataset').
        table_id: BigQuery table ID from which to drop the vector index
            (for example, 'example_embeddings').
    """
    client = bigquery.Client(project=project_id)
    # Target the example_vector_index provisioned on the embeddings table.
    index_name = "example_vector_index"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    sql = f"DROP VECTOR INDEX IF EXISTS `{index_name}` ON `{table_ref}`;"

    try:
        print(f"Dropping vector index {index_name} from table: {table_ref}")
        query_job = client.query(sql)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: table '{table_id}' or vector index '{index_name}' not found in "
            f"dataset '{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to drop vector index '{index_name}' on table '{table_id}' "
            f"in dataset '{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Index Name: {index_name}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Statement Type: {query_job.statement_type}")


# [END bigquery_drop_vector_index]
