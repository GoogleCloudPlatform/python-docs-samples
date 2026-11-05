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

# [START bigquery_read_biglake_gcs_storage_api]
import sys

from google.api_core import exceptions
from google.cloud import bigquery_storage_v1


def read_biglake_gcs_storage_api(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    """Reads projected columns from a BigLake table using the BigQuery Storage Read API.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the BigLake table
            (for example, 'example_dataset').
        table_id: BigLake table ID to read (for example, 'example_biglake_table').
    """
    client = bigquery_storage_v1.BigQueryReadClient()
    parent = f"projects/{project_id}"
    table_ref = f"projects/{project_id}/datasets/{dataset_id}/tables/{table_id}"

    # Project specific columns in the ReadSession to minimize network transfer from Cloud Storage.
    read_options = bigquery_storage_v1.types.ReadSession.TableReadOptions(
        selected_fields=["id", "label", "score"]
    )
    requested_session = bigquery_storage_v1.types.ReadSession(
        table=table_ref,
        data_format=bigquery_storage_v1.types.DataFormat.AVRO,
        read_options=read_options,
    )
    request = bigquery_storage_v1.types.CreateReadSessionRequest(
        parent=parent,
        read_session=requested_session,
        max_stream_count=1,
    )

    try:
        print(f"Creating Storage Read API session for BigLake table {table_ref}")
        session = client.create_read_session(request=request)
        rows_read = 0
        if session.streams:
            reader = client.read_rows(session.streams[0].name)
            for response in reader:
                rows_read += response.row_count
    except exceptions.NotFound as err:
        print(
            f"error: BigLake table '{table_id}' not found in dataset '{dataset_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to read BigLake table '{table_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Read Session: {session.name}")
    print(f"Rows Read: {rows_read}")
    print(f"Stream Count: {len(session.streams)}")


# [END bigquery_read_biglake_gcs_storage_api]
