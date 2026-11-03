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

# [START bigquery_create_manifest_biglake_table]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def create_manifest_biglake_table(
    project_id: str,
    dataset_id: str,
    connection_id: str,
    manifest_uri: str,
) -> None:
    """Creates a BigLake external table backed by a newline-delimited manifest file.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID where the BigLake table is created
            (for example, 'example_dataset').
        connection_id: Fully qualified BigQuery Cloud Resource connection ID
            (for example, 'example-project.us.example_biglake_conn').
        manifest_uri: Cloud Storage URI of the SymLinkTextInputFormat manifest file
            (for example, 'gs://example-bucket/manifests/symlink.manifest').
    """
    client = bigquery.Client(project=project_id)
    # Use a fixed table identifier inside the caller-supplied dataset.
    table_id = "example_manifest_biglake_table"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    # Setting file_set_spec_type to NEW_LINE_DELIMITED_MANIFEST tells BigQuery to resolve the
    # Parquet data files listed inside the manifest URI via the BigLake connection.
    sql = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{table_ref}`
        WITH CONNECTION `{connection_id}`
        OPTIONS (
          format = 'PARQUET',
          uris = ['{manifest_uri}'],
          file_set_spec_type = 'NEW_LINE_DELIMITED_MANIFEST'
        );
    """

    try:
        print(f"Creating manifest-backed BigLake table: {table_ref}")
        query_job = client.query(sql)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: dataset '{dataset_id}' or connection '{connection_id}' not found "
            f"for project '{project_id}' (manifest '{manifest_uri}'): {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create BigLake table '{table_id}' in dataset '{dataset_id}' "
            f"for project '{project_id}' (connection '{connection_id}', "
            f"manifest '{manifest_uri}'): {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Connection ID: {connection_id}")
    print("File Set Spec Type: NEW_LINE_DELIMITED_MANIFEST")
    print(f"Job ID: {query_job.job_id}")
    print(f"Manifest URI: {manifest_uri}")
    print(f"Statement Type: {query_job.statement_type}")


# [END bigquery_create_manifest_biglake_table]
