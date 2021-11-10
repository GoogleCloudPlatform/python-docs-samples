# Copyright 2020 Google LLC
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

# [START documentai_process_specialized_document]

# TODO(developer): Uncomment these variables before running the sample.
# project_id= 'YOUR_PROJECT_ID'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor in Cloud Console
# file_path = '/path/to/local/pdf'

def process_document_specialized_sample(
    project_id: str, location: str, processor_id: str, file_path: str
):
    from google.cloud import documentai_v1beta3 as documentai

    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = {}
    if location == "eu":
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Read the file into memory
    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "raw_document": document}

    # Recognizes text entities in the PDF document
    result = client.process_document(request=request)

    print("Document processing complete.\n")

    # Read fields specificly from the specalized US drivers license processor:
    # https://cloud.google.com/document-ai/docs/processors-list#processor_us-driver-license-parser
    # retriving data from other specalized processors follow a similar pattern.
    # For a complete list of processors see:
    # https://cloud.google.com/document-ai/docs/processors-list
    #
    # OCR and other data is also present in the quality processor's response.
    # Please see the OCR and other samples for how to parse other data in the
    # response.
    document = result.document
    print(f'Found {len(document.entities)} entities:')
    for entity in document.entities:
        # Fields detected. For a full list of fields for each processor see
        # the processor documentation:
        # https://cloud.google.com/document-ai/docs/processors-list
        key = entity.type_
        # some other value formats in addition to text are availible
        # e.g. dates: `entity.normalized_value.date_value.year`
        text_value = entity.text_anchor.content
        conf_percent = '{:.1%}'.format(entity.confidence)
        print(f'    * {repr(key)}: {repr(text_value)}({conf_percent} confident)')

# [END documentai_process_specialized_document]
