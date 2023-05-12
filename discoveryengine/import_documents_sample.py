# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# [START genappbuilder_import_documents]
from typing import Optional

from google.cloud import discoveryengine_v1beta as genappbuilder

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION" # Values: "global"
# search_engine_id = "YOUR_SEARCH_ENGINE_ID"

# Must specify either `gcs_uri` or (`bigquery_dataset` and `bigquery_table`)
# Format: `gs://bucket/directory/object.json` or `gs://bucket/directory/*.json`
# gcs_uri = "YOUR_GCS_PATH"
# bigquery_dataset = "YOUR_BIGQUERY_DATASET"
# bigquery_table = "YOUR_BIGQUERY_TABLE"


def import_documents_sample(
    project_id: str,
    location: str,
    search_engine_id: str,
    gcs_uri: Optional[str] = None,
    bigquery_dataset: Optional[str] = None,
    bigquery_table: Optional[str] = None,
) -> None:
    # Create a client
    client = genappbuilder.DocumentServiceClient()

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=search_engine_id,
        branch="default_branch",
    )

    if gcs_uri:
        request = genappbuilder.ImportDocumentsRequest(
            parent=parent,
            gcs_source=genappbuilder.GcsSource(
                input_uris=[gcs_uri], data_schema="custom"
            ),
            # Options: `FULL`, `INCREMENTAL`
            reconciliation_mode=genappbuilder.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
        )
    else:
        request = genappbuilder.ImportDocumentsRequest(
            parent=parent,
            bigquery_source=genappbuilder.BigQuerySource(
                project_id=project_id,
                dataset_id=bigquery_dataset,
                table_id=bigquery_table,
                data_schema="custom",
            ),
            # Options: `FULL`, `INCREMENTAL`
            reconciliation_mode=genappbuilder.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
        )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # Once the operation is complete,
    # get information from operation metadata
    metadata = genappbuilder.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)


# [END genappbuilder_import_documents]
