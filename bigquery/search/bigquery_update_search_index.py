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

# [START bigquery_update_search_index]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def update_search_index(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Updates an existing search index on a BigQuery table using ALTER SEARCH INDEX.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the indexed table
            (for example, 'example_dataset').
        table_id: BigQuery table ID whose search index will be updated
            (for example, 'example_table').
    """
    client = bigquery.Client(project=project_id)
    index_name = "example_search_index"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # Drop an unused column from the search index as a metadata-only update without rebuilding from scratch.
    sql = f"""
        ALTER SEARCH INDEX IF EXISTS `{index_name}`
        ON `{table_ref}`
        DROP COLUMN IF EXISTS category;
    """

    try:
        print(f"Updating search index {index_name} on table: {table_ref}")
        query_job = client.query(sql)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: table '{table_id}' or dataset '{dataset_id}' not found in "
            f"project '{project_id}' when updating search index '{index_name}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to update search index '{index_name}' on table "
            f"'{table_id}' in dataset '{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Index Name: {index_name}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Statement Type: {query_job.statement_type}")


# [END bigquery_update_search_index]
