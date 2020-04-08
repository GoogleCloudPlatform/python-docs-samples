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


# [START documentai_set_endpoint]
from google.cloud import documentai_v1beta2 as documentai


def set_endpoint(project_id='YOUR_PROJECT_ID',
                 input_uri='gs://cloud-samples-data/documentai/invoice.pdf'):
    """Process a single document with the Document AI API, including
    text extraction and entity extraction."""

    client = documentai.DocumentUnderstandingServiceClient(
        client_options={"api_endpoint": "eu-documentai.googleapis.com"})

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        gcs_source=gcs_source, mime_type='application/pdf')

    parent = "projects/{}/locations/europe-west2".format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config)

    document = client.process_document(request=request)

    # All text extracted from the document
    print("Document Text:")
    print(document.text)

    def _get_text(el):
        """Convert text offset indexes into text snippets.
        """
        response = ""
        # If a form field spans several lines, it will
        # be stored in different text segments.
        for segment in el.text_anchor.text_segments:
            start_index = segment.start_index
            end_index = segment.end_index
            response += document.text[start_index:end_index]
        return response

    for entity in document.entities:
        print("Entity type: {}".format(entity.type))
        print("Text: {}".format(_get_text(entity)))
        print("Mention text: {}\n".format(entity.mention_text))

# [END documentai_set_endpoint]
