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


from google.api_core.client_options import ClientOptions
from google.cloud import documentai

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# file_path = '/path/to/local/pdf'
# mime_type = 'application/pdf' # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types


def process_document_specialized_sample(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
):
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, file_path, mime_type
    )

    # Extract entities from a specialized document
    # Most specalized processors follow a similar pattern.
    # For a complete list of processors see:
    # https://cloud.google.com/document-ai/docs/processors-list
    #
    # OCR and other data is also present in the quality processor's response.
    # Please see the OCR and other samples for how to parse other data in the
    # response.

    print(f"Found {len(document.entities)} entities:")
    for entity in document.entities:
        print_entity(entity)
        # Print Nested Entities (if any)
        for prop in entity.properties:
            print_entity(prop)


def print_entity(entity: documentai.Document.Entity) -> None:
    # Fields detected. For a full list of fields for each processor see
    # the processor documentation:
    # https://cloud.google.com/document-ai/docs/processors-list
    key = entity.type_
    # some other value formats in addition to text are availible
    # e.g. dates: `entity.normalized_value.date_value.year`
    text_value = entity.text_anchor.content
    confidence = entity.confidence
    normalized_value = entity.normalized_value.text
    print(f"    * {repr(key)}: {repr(text_value)}({confidence:.1%} confident)")

    if normalized_value:
        print(f"    * Normalized Value: {repr(normalized_value)}")


def process_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> documentai.Document:
    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project_id/locations/location/processor/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    return result.document


# [END documentai_process_specialized_document]
