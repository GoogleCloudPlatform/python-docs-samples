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

# [START documentai_process_splitter_document]

from typing import Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# file_path = '/path/to/local/pdf'
# mime_type = 'application/pdf' # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types


def process_document_splitter_sample(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
):
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, file_path, mime_type
    )

    # Read the splitter output from a document splitter/classifier processor:
    # e.g. https://cloud.google.com/document-ai/docs/processors-list#processor_procurement-document-splitter
    # This processor only provides text for the document and information on how
    # to split the document on logical boundaries. To identify and extract text,
    # form elements, and entities please see other processors like the OCR, form,
    # and specalized processors.

    print(f"Found {len(document.entities)} subdocuments:")
    for entity in document.entities:
        conf_percent = f"{entity.confidence:.1%}"
        pages_range = page_refs_to_string(entity.page_anchor.page_refs)

        # Print subdocument type information, if available
        if entity.type_:
            print(
                f"{conf_percent} confident that {pages_range} a '{entity.type_}' subdocument."
            )
        else:
            print(f"{conf_percent} confident that {pages_range} a subdocument.")


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


def page_refs_to_string(
    page_refs: Sequence[documentai.Document.PageAnchor.PageRef],
) -> str:
    """Converts a page ref to a string describing the page or page range."""
    if len(page_refs) == 1:
        num = str(int(page_refs[0].page) + 1)
        return f"page {num} is"

    nums = ""
    for page_ref in page_refs:
        nums += f"{int(page_ref.page) + 1}, "
    return f"pages {nums[:-2]} are"


# [END documentai_process_splitter_document]
