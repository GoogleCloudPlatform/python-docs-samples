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


# [START documentai_parse_with_model]
from google.cloud import documentai_v1beta2 as documentai


def parse_with_model(
        project_id='YOUR_PROJECT_ID',
        input_uri='gs://cloud-samples-data/documentai/invoice.pdf',
        automl_model='YOUR_AUTOML_MODEL_NAME_HERE'):
    """Process a single document with the Document AI API with including
    text extraction and entity extraction.
    """

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        gcs_source=gcs_source, mime_type='application/pdf')

    automl_params = documentai.types.AutoMlParams(model=automl_model)

    parent = 'projects/{}/locations/us-central1'.format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config,
        automl_params=automl_params
        )

    document = client.process_document(request=request)

    for label in document.labels:
        print('Label detected: {}'.format(label.name))
        print('Confidence: {}'.format(label.confidence))

# [END documentai_parse_with_model]
