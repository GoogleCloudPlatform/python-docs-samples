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


# [START documentai_batch_parse_form_beta]
import re

from google.cloud import documentai_v1beta2 as documentai
from google.cloud import storage


def batch_parse_form(
    project_id="YOUR_PROJECT_ID",
    input_uri="gs://cloud-samples-data/documentai/form.pdf",
    destination_uri="gs://your-bucket-id/path/to/save/results/",
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

    # Improve form parsing results by providing key-value pair hints.
    # For each key hint, key is text that is likely to appear in the
    # document as a form field name (i.e. "DOB").
    # Value types are optional, but can be one or more of:
    # ADDRESS, LOCATION, ORGANIZATION, PERSON, PHONE_NUMBER, ID,
    # NUMBER, EMAIL, PRICE, TERMS, DATE, NAME
    key_value_pair_hints = [
        documentai.types.KeyValuePairHint(
            key="Emergency Contact", value_types=["NAME"]
        ),
        documentai.types.KeyValuePairHint(key="Referred By"),
    ]

    # Setting enabled=True enables form extraction
    form_extraction_params = documentai.types.FormExtractionParams(
        enabled=True, key_value_pair_hints=key_value_pair_hints
    )

    # Location can be 'us' or 'eu'
    parent = "projects/{}/locations/us".format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        input_config=input_config,
        output_config=output_config,
        form_extraction_params=form_extraction_params,
    )

    # Add each ProcessDocumentRequest to the batch request
    requests = []
    requests.append(request)

    batch_request = documentai.types.BatchProcessDocumentsRequest(
        parent=parent, requests=requests
    )

    operation = client.batch_process_documents(batch_request)

    # Wait for the operation to finish
    operation.result()

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


# [END documentai_batch_parse_form_beta]
