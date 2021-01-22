# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START documentai_batch_parse_table_beta]
import re

from google.cloud import documentai_v1beta2 as documentai
from google.cloud import storage


def batch_parse_table(
    project_id="YOUR_PROJECT_ID",
    input_uri="gs://cloud-samples-data/documentai/form.pdf",
    destination_uri="gs://your-bucket-id/path/to/save/results/",
    timeout=90
):
    """Parse a form"""

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        gcs_source=gcs_source, mime_type="application/pdf"
    )

    # where to write results
    output_config = documentai.types.OutputConfig(
        gcs_destination=documentai.types.GcsDestination(uri=destination_uri),
        pages_per_shard=1,  # Map one doc page to one output page
    )

    # Improve table parsing results by providing bounding boxes
    # specifying where the box appears in the document (optional)
    table_bound_hints = [
        documentai.types.TableBoundHint(
            page_number=1,
            bounding_box=documentai.types.BoundingPoly(
                # Define a polygon around tables to detect
                # Each vertice coordinate must be a number between 0 and 1
                normalized_vertices=[
                    # Top left
                    documentai.types.geometry.NormalizedVertex(x=0, y=0),
                    # Top right
                    documentai.types.geometry.NormalizedVertex(x=1, y=0),
                    # Bottom right
                    documentai.types.geometry.NormalizedVertex(x=1, y=1),
                    # Bottom left
                    documentai.types.geometry.NormalizedVertex(x=0, y=1),
                ]
            ),
        )
    ]

    # Setting enabled=True enables form extraction
    table_extraction_params = documentai.types.TableExtractionParams(
        enabled=True, table_bound_hints=table_bound_hints
    )

    # Location can be 'us' or 'eu'
    parent = "projects/{}/locations/us".format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        input_config=input_config,
        output_config=output_config,
        table_extraction_params=table_extraction_params,
    )

    requests = []
    requests.append(request)

    batch_request = documentai.types.BatchProcessDocumentsRequest(
        parent=parent, requests=requests
    )

    operation = client.batch_process_documents(batch_request)

    # Wait for the operation to finish
    operation.result(timeout)

    # Results are written to GCS. Use a regex to find
    # output files
    match = re.match(r"gs://([^/]+)/(.+)", destination_uri)
    output_bucket = match.group(1)
    prefix = match.group(2)

    storage_client = storage.client.Client()
    bucket = storage_client.get_bucket(output_bucket)
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print("Output files:")
    for blob in blob_list:
        print(blob.name)


# [END documentai_batch_parse_table_beta]
