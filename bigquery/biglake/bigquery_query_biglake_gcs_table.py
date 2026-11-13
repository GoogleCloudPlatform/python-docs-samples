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

# [START bigquery_query_biglake_gcs_table]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def query_biglake_gcs_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Queries a BigLake table backed by Cloud Storage using GoogleSQL.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the BigLake table
            (for example, 'example_dataset').
        table_id: BigLake table ID to query (for example, 'example_biglake_table').
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # BigLake delegates Cloud Storage access to the table's Cloud Resource connection,
    # allowing standard SQL queries with fine-grained governance.
    sql = f"""
        SELECT
          id,
          label,
          score
        FROM `{table_ref}`
        ORDER BY score DESC, id ASC
        LIMIT 10;
    """

    try:
        print(f"Querying BigLake table: {table_ref}")
        query_job = client.query(sql)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: BigLake table '{table_id}' not found in dataset '{dataset_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to query BigLake table '{table_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Rows Returned: {len(rows)}")


# [END bigquery_query_biglake_gcs_table]
