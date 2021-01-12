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


def set_endpoint(
    project_id="YOUR_PROJECT_ID",
    input_uri="gs://cloud-samples-data/documentai/invoice.pdf",
):
    """Process a single document with the Document AI API, including
    text extraction and entity extraction."""

    # [START documentai_set_endpoint_beta]
    from google.cloud import documentai_v1beta2 as documentai

    client = documentai.DocumentUnderstandingServiceClient(
        client_options={"api_endpoint": "eu-documentai.googleapis.com"}
    )
    # [END documentai_set_endpoint_beta]

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        gcs_source=gcs_source, mime_type="application/pdf"
    )

    # Location can be 'us' or 'eu'
    parent = "projects/{}/locations/eu".format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent, input_config=input_config
    )

    document = client.process_document(request=request)

    # All text extracted from the document
    print("Document Text: {}".format(document.text))
