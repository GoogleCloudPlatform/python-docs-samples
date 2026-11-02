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

# [START bigquery_query_manifest_external_table]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def query_manifest_external_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    manifest_uri: str,
) -> None:
    """Configures a newline-delimited manifest on an external table and queries it.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the external table
            (for example, 'example_dataset').
        table_id: BigQuery external table ID
            (for example, 'example_manifest_table').
        manifest_uri: Cloud Storage URI of the newline-delimited manifest file
            (for example, 'gs://example-bucket/manifests/symlink.manifest').
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Setting FILE_SET_SPEC_TYPE_NEW_LINE_DELIMITED_MANIFEST tells BigQuery to treat each line
    # in manifest_uri as a Cloud Storage data file URI rather than reading the manifest as CSV data.
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [manifest_uri]
    external_config.file_set_spec_type = (
        "FILE_SET_SPEC_TYPE_NEW_LINE_DELIMITED_MANIFEST"
    )

    table = bigquery.Table(table_ref)
    table.external_data_configuration = external_config

    query = (
        "SELECT id, label, score " f"FROM `{table_ref}` " "ORDER BY id ASC " "LIMIT 10"
    )

    try:
        print(f"Configuring manifest URI and querying external table: {table_ref}")
        client.update_table(table, ["external_data_configuration"])
        query_job = client.query(query)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: manifest external table '{table_id}' in dataset '{dataset_id}' "
            f"for project '{project_id}' (manifest '{manifest_uri}') was not found: {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: could not query manifest external table '{table_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}' (manifest '{manifest_uri}'): {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Manifest URI: {manifest_uri}")
    print(f"Rows Returned: {len(rows)}")


# [END bigquery_query_manifest_external_table]
