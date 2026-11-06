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

# [START bigquery_query_external_bigtable]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def query_external_bigtable(
    project_id: str,
    bigtable_instance_id: str,
    bigtable_table_id: str,
) -> None:
    """Configures and queries a temporary BigQuery external table backed by Cloud Bigtable.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        bigtable_instance_id: Cloud Bigtable instance ID hosting the source table
            (for example, 'example-bt-instance').
        bigtable_table_id: Cloud Bigtable table ID containing the column family
            (for example, 'example_bt_table').
    """
    client = bigquery.Client(project=project_id)
    temp_table_name = "example_bigtable_temp"
    source_uri = (
        f"https://googleapis.com/bigtable/projects/{project_id}"
        f"/instances/{bigtable_instance_id}/tables/{bigtable_table_id}"
    )

    # Map the Cloud Bigtable column family into a temporary table definition for a single query job.
    external_config = bigquery.ExternalConfig("BIGTABLE")
    external_config.source_uris = [source_uri]
    external_config.bigtable_options.read_rowkey_as_string = True
    family = bigquery.BigtableColumnFamily()
    family.family_id = "stats_summary"
    family.type_ = "STRING"
    family.encoding = "TEXT"
    external_config.bigtable_options.column_families = [family]

    job_config = bigquery.QueryJobConfig(
        table_definitions={temp_table_name: external_config}
    )
    sql = f"""
        SELECT
          rowkey,
          stats_summary
        FROM `{temp_table_name}`
        ORDER BY rowkey ASC
        LIMIT 10;
    """

    try:
        print(f"Querying temporary Cloud Bigtable table mapped to {source_uri}")
        query_job = client.query(sql, job_config=job_config)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: Cloud Bigtable table '{bigtable_table_id}' in instance "
            f"'{bigtable_instance_id}' not found for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to query Cloud Bigtable table '{bigtable_table_id}' in "
            f"instance '{bigtable_instance_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {source_uri}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Rows Returned: {len(rows)}")
    print(f"Temporary Table: {temp_table_name}")


# [END bigquery_query_external_bigtable]
