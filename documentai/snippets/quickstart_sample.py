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

from google.cloud.documentai_v1.types.document import Document
from google.cloud.documentai_v1.types.processor import Processor


def quickstart(
    project_id: str,
    location: str,
    file_path: str,
    processor_display_name: str ,
) -> tuple[Processor, Document]:
    # [START documentai_quickstart]
    from google.api_core.client_options import ClientOptions
    from google.cloud import documentai_v1  # type: ignore

    # TODO(developer): Update and uncomment these variables before running the sample.
    # project_id = "MY_PROJECT_ID"

    # Processor location. For example: "us" or "eu".
    # location = "MY_PROCESSOR_LOCATION"

    # Path for file to process.
    # file_path = "/path/to/local/pdf"

    # Processor display name must be unique per project.
    # processor_display_name = "MY_PROCESSOR_DISPLAY_NAME"

    # Set `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    # Initialize Document AI client.
    client = documentai_v1.DocumentProcessorServiceClient(client_options=opts)

    # Get the full resource name of the location.
    # For example: `projects/{project_id}/locations/{location}`
    parent = client.common_location_path(project_id, location)

    # Create a Processor.
    # For available types, refer to https://cloud.google.com/document-ai/docs/create-processor
    processor = client.create_processor(
        parent=parent,
        processor=documentai_v1.Processor(
            type_="OCR_PROCESSOR",
            display_name=processor_display_name,
        ),
    )

    # Print the processor information.
    print(f"Processor Name: {processor.name}")

    # Read the file into memory.
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data.
    # For supported MIME types, refer to https://cloud.google.com/document-ai/docs/file-types
    raw_document = documentai_v1.RawDocument(
        content=image_content,
        mime_type="application/pdf",
    )

    # Configure the process request.
    # `processor.name` is the full resource name of the processor,
    # For example: `projects/{project_id}/locations/{location}/processors/{processor_id}`
    request = documentai_v1.ProcessRequest(name=processor.name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    # Read the text recognition output from the processor.
    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    print("The document contains the following text:")
    print(document.text)
    # [END documentai_quickstart]

    return processor, document
