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


# [START documentai_batch_process_document]
import re

from google.cloud import documentai_v1beta3 as documentai
from google.cloud import storage

# TODO(developer): Uncomment these variables before running the sample.
# project_id= 'YOUR_PROJECT_ID'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor in Cloud Console
# gcs_input_uri = "YOUR_INPUT_URI"
# gcs_output_uri = "YOUR_OUTPUT_BUCKET_URI"
# gcs_output_uri_prefix = "YOUR_OUTPUT_URI_PREFIX"


def batch_process_documents(
    project_id,
    location,
    processor_id,
    gcs_input_uri,
    gcs_output_uri,
    gcs_output_uri_prefix,
    timeout: int = 300,
):

    client = documentai.DocumentProcessorServiceClient()

    destination_uri = f"{gcs_output_uri}/{gcs_output_uri_prefix}/"

    # 'mime_type' can be 'application/pdf', 'image/tiff',
    # and 'image/gif', or 'application/json'
    input_config = documentai.types.document_processor_service.BatchProcessRequest.BatchInputConfig(
        gcs_source=gcs_input_uri, mime_type="application/pdf"
    )

    # Where to write results
    output_config = documentai.types.document_processor_service.BatchProcessRequest.BatchOutputConfig(
        gcs_destination=destination_uri
    )

    # Location can be 'us' or 'eu'
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    request = documentai.types.document_processor_service.BatchProcessRequest(
        name=name,
        input_configs=[input_config],
        output_config=output_config,
    )

    operation = client.batch_process_documents(request)

    # Wait for the operation to finish
    operation.result(timeout=timeout)

    # Results are written to GCS. Use a regex to find
    # output files
    match = re.match(r"gs://([^/]+)/(.+)", destination_uri)
    output_bucket = match.group(1)
    prefix = match.group(2)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(output_bucket)
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print("Output files:")

    for i, blob in enumerate(blob_list):
        # If JSON file, download the contents of this blob as a bytes object.
        if ".json" in blob.name:
            blob_as_bytes = blob.download_as_bytes()

            document = documentai.types.Document.from_json(blob_as_bytes)
            print(f"Fetched file {i + 1}")

            # For a full list of Document object attributes, please reference this page:
            # https://cloud.google.com/document-ai/docs/reference/rpc/google.cloud.documentai.v1beta3#document

            # Read the text recognition output from the processor
            for page in document.pages:
                for form_field in page.form_fields:
                    field_name = get_text(form_field.field_name, document)
                    field_value = get_text(form_field.field_value, document)
                    print("Extracted key value pair:")
                    print(f"\t{field_name}, {field_value}")
                for paragraph in document.pages:
                    paragraph_text = get_text(paragraph.layout, document)
                    print(f"Paragraph text:\n{paragraph_text}")
        else:
            print(f"Skipping non-supported file type {blob.name}")


# Extract shards from the text field
def get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response


# [END documentai_batch_process_document]
