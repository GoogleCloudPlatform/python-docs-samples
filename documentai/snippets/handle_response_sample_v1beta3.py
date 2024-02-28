# Copyright 2023 Google LLC
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

# [START documentai_process_summarizer_document]
# [START documentai_process_custom_extractor_document]
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1beta3 as documentai


# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_PROCESSOR_LOCATION" # Format is "us" or "eu"
# processor_id = "YOUR_PROCESSOR_ID" # Create processor before running sample
# processor_version = "rc" # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
# file_path = "/path/to/local/pdf"
# mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types

# [END documentai_process_custom_extractor_document]


def process_document_summarizer_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> None:
    # For supported options, refer to:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions#summaryoptions
    summary_options = documentai.SummaryOptions(
        length=documentai.SummaryOptions.Length.BRIEF,
        format=documentai.SummaryOptions.Format.BULLETS,
    )

    properties = [
        documentai.DocumentSchema.EntityType.Property(
            name="summary",
            value_type="string",
            occurrence_type=documentai.DocumentSchema.EntityType.Property.OccurrenceType.REQUIRED_ONCE,
            property_metadata=documentai.PropertyMetadata(
                field_extraction_metadata=documentai.FieldExtractionMetadata(
                    summary_options=summary_options
                )
            ),
        )
    ]

    # Optional: Request specific summarization format other than the default
    # for the processor version.
    process_options = documentai.ProcessOptions(
        schema_override=documentai.DocumentSchema(
            entity_types=[
                documentai.DocumentSchema.EntityType(
                    name="summary_document_type",
                    base_types=["document"],
                    properties=properties,
                )
            ]
        )
    )

    # Online processing request to Document AI
    document = process_document(
        project_id,
        location,
        processor_id,
        processor_version,
        file_path,
        mime_type,
        process_options=process_options,
    )

    for entity in document.entities:
        print_entity(entity)
        # Print Nested Entities (if any)
        for prop in entity.properties:
            print_entity(prop)


# [END documentai_process_summarizer_document]

# [START documentai_process_custom_extractor_document]


def process_document_custom_extractor_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> None:
    # Entities to extract from Foundation Model CDE
    properties = [
        documentai.DocumentSchema.EntityType.Property(
            name="invoice_id",
            value_type="string",
            occurrence_type=documentai.DocumentSchema.EntityType.Property.OccurrenceType.REQUIRED_ONCE,
        ),
        documentai.DocumentSchema.EntityType.Property(
            name="notes",
            value_type="string",
            occurrence_type=documentai.DocumentSchema.EntityType.Property.OccurrenceType.REQUIRED_ONCE,
        ),
        documentai.DocumentSchema.EntityType.Property(
            name="terms",
            value_type="string",
            occurrence_type=documentai.DocumentSchema.EntityType.Property.OccurrenceType.REQUIRED_ONCE,
        ),
    ]
    # Optional: For Generative AI processors, request different fields than the
    # schema for a processor version
    process_options = documentai.ProcessOptions(
        schema_override=documentai.DocumentSchema(
            display_name="CDE Schema",
            description="Document Schema for the CDE Processor",
            entity_types=[
                documentai.DocumentSchema.EntityType(
                    name="custom_extraction_document_type",
                    base_types=["document"],
                    properties=properties,
                )
            ],
        )
    )

    # Online processing request to Document AI
    document = process_document(
        project_id,
        location,
        processor_id,
        processor_version,
        file_path,
        mime_type,
        process_options=process_options,
    )

    for entity in document.entities:
        print_entity(entity)
        # Print Nested Entities (if any)
        for prop in entity.properties:
            print_entity(prop)


# [START documentai_process_summarizer_document]
def print_entity(entity: documentai.Document.Entity) -> None:
    # Fields detected. For a full list of fields for each processor see
    # the processor documentation:
    # https://cloud.google.com/document-ai/docs/processors-list
    key = entity.type_

    # Some other value formats in addition to text are availible
    # e.g. dates: `entity.normalized_value.date_value.year`
    text_value = entity.text_anchor.content
    confidence = entity.confidence
    normalized_value = entity.normalized_value.text
    print(f"    * {repr(key)}: {repr(text_value)}({confidence:.1%} confident)")

    if normalized_value:
        print(f"    * Normalized Value: {repr(normalized_value)}")


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor version, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    # You must create a processor before running this sample.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
        # Only supported for Document OCR processor
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    return result.document


# [END documentai_process_summarizer_document]
# [END documentai_process_custom_extractor_document]
