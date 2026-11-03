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

# [START bigquery_get_search_index_status]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def get_search_index_status(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Queries INFORMATION_SCHEMA.SEARCH_INDEXES to inspect search index status.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the indexed table
            (for example, 'example_dataset').
        table_id: BigQuery table ID to inspect search indexes for
            (for example, 'example_table').
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # Parameterize the table_name filter when querying INFORMATION_SCHEMA.SEARCH_INDEXES.
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("table_id", "STRING", table_id),
        ]
    )
    sql = f"""
        SELECT
          index_name,
          index_status,
          coverage_percentage
        FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.SEARCH_INDEXES`
        WHERE table_name = @table_id;
    """

    try:
        print(f"Checking search index status for table: {table_ref}")
        query_job = client.query(sql, job_config=job_config)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: dataset '{dataset_id}' or table '{table_id}' not found in "
            f"project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to get search index status for table '{table_id}' in "
            f"dataset '{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    index_name = rows[0].index_name if rows else "NONE"
    index_status = rows[0].index_status if rows else "NONE"
    coverage_percentage = rows[0].coverage_percentage if rows else 0
    print(f"Resource ID: {table_ref}")
    print(f"Index Count: {len(rows)}")
    print(f"Index Name: {index_name}")
    print(f"Index Status: {index_status}")
    print(f"Coverage Percentage: {coverage_percentage}%")
    print(f"Job ID: {query_job.job_id}")


# [END bigquery_get_search_index_status]
