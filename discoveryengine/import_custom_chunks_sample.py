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

"""Bring Your Own Chunks (BYOC) import sample for Agent Search."""

# [START genappbuilder_import_custom_chunks]
from google.api_core.operation import Operation
from google.cloud import discoveryengine_v1 as discoveryengine


def import_custom_chunk_documents(
    project_id: str,
    location: str,
    data_store_id: str,
    gcs_uri: str,
) -> Operation:
  """Imports pre-chunked JSON documents from Cloud Storage into an Agent Search data store.

  When bringing pre-chunked documents (e.g., from LangChain, LlamaIndex, or
  custom semantic splitters), the JSON files in Cloud Storage must adhere to the
  Bring Your Own Chunks (BYOC) schema with a top-level `documentMetadata` object
  and a `chunks` array:

  ```json
  {
    "documentMetadata": {
      "title": "Example Document Title",
      "uri": "https://example.com/doc.pdf",
      "structData": {
        "category": "technical",
        "rating": 4.5
      }
    },
    "chunks": [
      {
        "id": "chunk_0",
        "content": "First section text...",
        "pageSpan": {
          "pageStart": 1,
          "pageEnd": 1
        }
      }
    ]
  }
  ```

  Args:
      project_id: Google Cloud project ID or project number.
      location: Data store location (e.g., 'global', 'us', 'eu').
      data_store_id: Target data store ID.
      gcs_uri: Cloud Storage URI of BYOC JSON files (e.g.,
        'gs://my-bucket/chunks/*.json').

  Returns:
      The Long-Running Operation (Operation) for the document import.
  """
  client = discoveryengine.DocumentServiceClient()

  # Document branch 0 is the default serving branch
  parent = (
      f"projects/{project_id}/locations/{location}/collections/default_collection"
      f"/dataStores/{data_store_id}/branches/0"
  )

  request = discoveryengine.ImportDocumentsRequest(
      parent=parent,
      gcs_source=discoveryengine.GcsSource(
          input_uris=[gcs_uri],
          data_schema="custom",
      ),
      # FULL reconciliation replaces the dataset; INCREMENTAL adds/updates
      reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
  )

  operation = client.import_documents(request=request)
  print(f"Triggered BYOC Document Import LRO: {operation.operation.name}")
  return operation


# [END genappbuilder_import_custom_chunks]
