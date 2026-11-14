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

# [START bigquery_upgrade_manifest_biglake_table]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def upgrade_manifest_biglake_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    connection_id: str,
    manifest_uri: str,
) -> None:
    """Upgrades a manifest external table to a BigLake table with metadata caching.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the external table
            (for example, 'example_dataset').
        table_id: BigQuery external table ID to upgrade
            (for example, 'example_manifest_table').
        connection_id: Fully qualified BigQuery Cloud Resource connection ID
            (for example, 'example-project.us.example_biglake_conn').
        manifest_uri: Cloud Storage URI of the SymLinkTextInputFormat manifest file
            (for example, 'gs://example-bucket/manifests/symlink.manifest').
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # Upgrading the manifest external table with a Cloud Resource connection and AUTOMATIC metadata
    # caching accelerates open-table-format reads and enforces BigLake governance.
    sql = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{table_ref}`
        WITH CONNECTION `{connection_id}`
        OPTIONS (
          format = 'PARQUET',
          uris = ['{manifest_uri}'],
          file_set_spec_type = 'NEW_LINE_DELIMITED_MANIFEST',
          max_staleness = INTERVAL 1 HOUR,
          metadata_cache_mode = 'AUTOMATIC'
        );
        SELECT
          id,
          label,
          score
        FROM `{table_ref}`
        ORDER BY id ASC
        LIMIT 10;
    """

    try:
        print(
            f"Upgrading manifest external table to BigLake with metadata caching: {table_ref}"
        )
        query_job = client.query(sql)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: manifest external table '{table_id}' or connection '{connection_id}' "
            f"not found in dataset '{dataset_id}' for project '{project_id}' "
            f"(manifest '{manifest_uri}'): {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to upgrade manifest external table '{table_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}' (connection '{connection_id}', "
            f"manifest '{manifest_uri}'): {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Connection ID: {connection_id}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Manifest URI: {manifest_uri}")
    print("Metadata Cache Mode: AUTOMATIC")
    print(f"Rows Returned: {len(rows)}")


# [END bigquery_upgrade_manifest_biglake_table]
