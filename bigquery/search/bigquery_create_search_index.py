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

# [START bigquery_create_search_index]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def create_search_index(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Creates a full-text search index across all columns of a BigQuery table.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the target table
            (for example, 'example_dataset').
        table_id: BigQuery table ID to index (for example, 'example_table').
    """
    client = bigquery.Client(project=project_id)
    # Use a fixed search index name on the caller-supplied table.
    index_name = "example_search_index"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # Indexing ALL COLUMNS enables full-text SEARCH queries across every STRING or JSON field.
    sql = f"""
        CREATE SEARCH INDEX IF NOT EXISTS `{index_name}`
        ON `{table_ref}`(ALL COLUMNS);
    """

    try:
        print(f"Creating search index {index_name} on table: {table_ref}")
        query_job = client.query(sql)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: table '{table_id}' or dataset '{dataset_id}' not found "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create search index '{index_name}' on table "
            f"'{table_id}' in dataset '{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Index Name: {index_name}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Statement Type: {query_job.statement_type}")


# [END bigquery_create_search_index]
