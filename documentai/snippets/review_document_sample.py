# Copyright 2022 Google LLC
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

# [START documentai_review_document]

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# file_path = '/path/to/local/pdf'
# mime_type = 'application/pdf'  # https://cloud.google.com/document-ai/docs/file-types


def review_document_sample(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    # Create a client
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # Make Processing Request
    inline_document = process_document(
        project_id, location, processor_id, file_path, mime_type
    )

    # Get the full resource name of the human review config, e.g.:
    # projects/project_id/locations/location/processor/processor_id/humanReviewConfig
    human_review_config = client.human_review_config_path(
        project_id, location, processor_id
    )

    # Options are DEFAULT, URGENT
    priority = documentai.ReviewDocumentRequest.Priority.DEFAULT

    # Configure the human review request
    request = documentai.ReviewDocumentRequest(
        inline_document=inline_document,
        human_review_config=human_review_config,
        enable_schema_validation=False,
        priority=priority,
    )

    # Make a request for human review of the processed document
    operation = client.review_document(request=request)

    # Print operation name, can be used to check status of the request
    print(operation.operation.name)


def process_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> documentai.Document:
    # You must set the api_endpoint if you use a location other than 'us'.
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


# [END documentai_review_document]
