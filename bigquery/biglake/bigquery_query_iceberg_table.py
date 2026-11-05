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

# [START bigquery_query_iceberg_table]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def query_iceberg_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    connection_id: str,
    metadata_uri: str,
) -> None:
    """Refreshes an Apache Iceberg external table metadata snapshot and queries it.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the Iceberg external table
            (for example, 'example_dataset').
        table_id: BigQuery Iceberg external table ID
            (for example, 'example_iceberg_table').
        connection_id: Fully qualified BigQuery Cloud Resource connection ID
            (for example, 'example-project.us.example_iceberg_conn').
        metadata_uri: Cloud Storage URI of the Apache Iceberg metadata JSON file
            (for example, 'gs://example-bucket/warehouse/db/table/metadata/v2.metadata.json').
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # BigQuery Iceberg external tables point to a specific Iceberg metadata JSON snapshot;
    # re-running CREATE OR REPLACE EXTERNAL TABLE updates the snapshot URI with schema autodetection.
    query = (
        f"CREATE OR REPLACE EXTERNAL TABLE `{table_ref}` "
        f"WITH CONNECTION `{connection_id}` "
        "OPTIONS ("
        "  format = 'ICEBERG',"
        f"  uris = ['{metadata_uri}']"
        "); "
        "SELECT order_id, user_id, status, num_of_item "
        f"FROM `{table_ref}` "
        "ORDER BY order_id ASC;"
    )

    try:
        print(f"Refreshing Iceberg metadata and querying table: {table_ref}")
        query_job = client.query(query)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: Apache Iceberg table '{table_id}' in dataset '{dataset_id}' "
            f"for project '{project_id}' (connection '{connection_id}', "
            f"metadata '{metadata_uri}') was not found: {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: could not refresh or query Apache Iceberg table '{table_id}' "
            f"in dataset '{dataset_id}' for project '{project_id}' "
            f"(connection '{connection_id}', metadata '{metadata_uri}'): {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Metadata URI: {metadata_uri}")
    print(f"Rows Returned: {len(rows)}")


# [END bigquery_query_iceberg_table]
