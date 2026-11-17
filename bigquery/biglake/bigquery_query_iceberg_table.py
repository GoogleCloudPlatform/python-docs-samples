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
    ddl_sql = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{table_ref}`
        WITH CONNECTION `{connection_id}`
        OPTIONS (
          format = 'ICEBERG',
          uris = ['{metadata_uri}']
        );
    """
    select_sql = f"""
        SELECT
          order_id,
          user_id,
          status,
          num_of_item
        FROM `{table_ref}`
        ORDER BY order_id ASC;
    """

    print(f"Refreshing Iceberg metadata and querying table: {table_ref}")
    client.query(ddl_sql).result()

    query_job = client.query(select_sql)
    rows = list(query_job.result())

    print(f"Resource ID: {table_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Metadata URI: {metadata_uri}")
    print(f"Rows Returned: {len(rows)}")


# [END bigquery_query_iceberg_table]
