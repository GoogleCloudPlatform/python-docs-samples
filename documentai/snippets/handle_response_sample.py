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

# [START documentai_process_ocr_document]
# [START documentai_process_form_document]
# [START documentai_process_specialized_document]
# [START documentai_process_splitter_document]
from typing import Optional, Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_PROCESSOR_LOCATION" # Format is "us" or "eu"
# processor_id = "YOUR_PROCESSOR_ID" # Create processor before running sample
# processor_version = "rc" # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
# file_path = "/path/to/local/pdf"
# mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types


# [END documentai_process_ocr_document]
# [END documentai_process_form_document]
# [END documentai_process_specialized_document]
# [END documentai_process_splitter_document]


# [START documentai_process_ocr_document]
def process_document_ocr_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> None:
    # Optional: Additional configurations for Document OCR Processor.
    # For more information: https://cloud.google.com/document-ai/docs/document-ocr
    process_options = documentai.ProcessOptions(
        ocr_config=documentai.OcrConfig(
            compute_style_info=True,
            enable_native_pdf_parsing=True,
            enable_image_quality_scores=True,
            enable_symbol=True,
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

    text = document.text
    print(f"Full document text: {text}\n")
    print(f"There are {len(document.pages)} page(s) in this document.\n")

    for page in document.pages:
        print(f"Page {page.page_number}:")
        print_page_dimensions(page.dimension)
        print_detected_langauges(page.detected_languages)

        print_blocks(page.blocks, text)
        print_paragraphs(page.paragraphs, text)
        print_lines(page.lines, text)
        print_tokens(page.tokens, text)

        if page.symbols:
            print_symbols(page.symbols, text)

        if page.image_quality_scores:
            print_image_quality_scores(page.image_quality_scores)

    if document.text_styles:
        print_styles(document.text_styles, text)


def print_page_dimensions(dimension: documentai.Document.Page.Dimension) -> None:
    print(f"    Width: {str(dimension.width)}")
    print(f"    Height: {str(dimension.height)}")


def print_detected_langauges(
    detected_languages: Sequence[documentai.Document.Page.DetectedLanguage],
) -> None:
    print("    Detected languages:")
    for lang in detected_languages:
        print(f"        {lang.language_code} ({lang.confidence:.1%} confidence)")


def print_blocks(blocks: Sequence[documentai.Document.Page.Block], text: str) -> None:
    print(f"    {len(blocks)} blocks detected:")
    first_block_text = layout_to_text(blocks[0].layout, text)
    print(f"        First text block: {repr(first_block_text)}")
    last_block_text = layout_to_text(blocks[-1].layout, text)
    print(f"        Last text block: {repr(last_block_text)}")


def print_paragraphs(
    paragraphs: Sequence[documentai.Document.Page.Paragraph], text: str
) -> None:
    print(f"    {len(paragraphs)} paragraphs detected:")
    first_paragraph_text = layout_to_text(paragraphs[0].layout, text)
    print(f"        First paragraph text: {repr(first_paragraph_text)}")
    last_paragraph_text = layout_to_text(paragraphs[-1].layout, text)
    print(f"        Last paragraph text: {repr(last_paragraph_text)}")


def print_lines(lines: Sequence[documentai.Document.Page.Line], text: str) -> None:
    print(f"    {len(lines)} lines detected:")
    first_line_text = layout_to_text(lines[0].layout, text)
    print(f"        First line text: {repr(first_line_text)}")
    last_line_text = layout_to_text(lines[-1].layout, text)
    print(f"        Last line text: {repr(last_line_text)}")


def print_tokens(tokens: Sequence[documentai.Document.Page.Token], text: str) -> None:
    print(f"    {len(tokens)} tokens detected:")
    first_token_text = layout_to_text(tokens[0].layout, text)
    first_token_break_type = tokens[0].detected_break.type_.name
    print(f"        First token text: {repr(first_token_text)}")
    print(f"        First token break type: {repr(first_token_break_type)}")
    last_token_text = layout_to_text(tokens[-1].layout, text)
    last_token_break_type = tokens[-1].detected_break.type_.name
    print(f"        Last token text: {repr(last_token_text)}")
    print(f"        Last token break type: {repr(last_token_break_type)}")


def print_symbols(
    symbols: Sequence[documentai.Document.Page.Symbol], text: str
) -> None:
    print(f"    {len(symbols)} symbols detected:")
    first_symbol_text = layout_to_text(symbols[0].layout, text)
    print(f"        First symbol text: {repr(first_symbol_text)}")
    last_symbol_text = layout_to_text(symbols[-1].layout, text)
    print(f"        Last symbol text: {repr(last_symbol_text)}")


def print_image_quality_scores(
    image_quality_scores: documentai.Document.Page.ImageQualityScores,
) -> None:
    print(f"    Quality score: {image_quality_scores.quality_score:.1%}")
    print("    Detected defects:")

    for detected_defect in image_quality_scores.detected_defects:
        print(f"        {detected_defect.type_}: {detected_defect.confidence:.1%}")


def print_styles(styles: Sequence[documentai.Document.Style], text: str) -> None:
    print(f"    {len(styles)} styles detected:")
    first_style_text = layout_to_text(styles[0].layout, text)
    print(f"        First style text: {repr(first_style_text)}")
    print(f"           Color: {styles[0].color}")
    print(f"           Background Color: {styles[0].background_color}")
    print(f"           Font Weight: {styles[0].font_weight}")
    print(f"           Text Style: {styles[0].text_style}")
    print(f"           Text Decoration: {styles[0].text_decoration}")
    print(f"           Font Size: {styles[0].font_size.size}{styles[0].font_size.unit}")
    print(f"           Font Family: {styles[0].font_family}")


# [END documentai_process_ocr_document]
# [START documentai_process_form_document]
def process_document_form_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
    )

    # Read the table and form fields output from the processor
    # The form processor also contains OCR data. For more information
    # on how to parse OCR data please see the OCR sample.

    text = document.text
    print(f"Full document text: {repr(text)}\n")
    print(f"There are {len(document.pages)} page(s) in this document.")

    # Read the form fields and tables output from the processor
    for page in document.pages:
        print(f"\n\n**** Page {page.page_number} ****")

        print(f"\nFound {len(page.tables)} table(s):")
        for table in page.tables:
            num_columns = len(table.header_rows[0].cells)
            num_rows = len(table.body_rows)
            print(f"Table with {num_columns} columns and {num_rows} rows:")

            # Print header rows
            print("Columns:")
            print_table_rows(table.header_rows, text)
            # Print body rows
            print("Table body data:")
            print_table_rows(table.body_rows, text)

        print(f"\nFound {len(page.form_fields)} form field(s):")
        for field in page.form_fields:
            name = layout_to_text(field.field_name, text)
            value = layout_to_text(field.field_value, text)
            print(f"    * {repr(name.strip())}: {repr(value.strip())}")

    # Supported in version `pretrained-form-parser-v2.0-2022-11-10` and later.
    # For more information: https://cloud.google.com/document-ai/docs/form-parser
    if document.entities:
        print(f"Found {len(document.entities)} generic entities:")
        for entity in document.entities:
            print_entity(entity)
            # Print Nested Entities
            for prop in entity.properties:
                print_entity(prop)

    return document


def print_table_rows(
    table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
) -> None:
    for table_row in table_rows:
        row_text = ""
        for cell in table_row.cells:
            cell_text = layout_to_text(cell.layout, text)
            row_text += f"{repr(cell_text.strip())} | "
        print(row_text)


# [END documentai_process_form_document]


# [START documentai_process_specialized_document]
def process_document_specialized_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> None:
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
    )

    # Print extracted entities from entity extraction processor output.
    # For a complete list of processors see:
    # https://cloud.google.com/document-ai/docs/processors-list
    #
    # OCR and other data is also present in the processor's response.
    # Refer to the OCR samples for how to parse other data in the response.

    print(f"Found {len(document.entities)} entities:")
    for entity in document.entities:
        print_entity(entity)
        # Print Nested Entities (if any)
        for prop in entity.properties:
            print_entity(prop)


# [START documentai_process_form_document]
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


# [END documentai_process_form_document]
# [END documentai_process_specialized_document]


# [START documentai_process_splitter_document]
def process_document_splitter_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> None:
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
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


def page_refs_to_string(
    page_refs: Sequence[documentai.Document.PageAnchor.PageRef],
) -> str:
    """Converts a page ref to a string describing the page or page range."""
    pages = [str(int(page_ref.page) + 1) for page_ref in page_refs]
    if len(pages) == 1:
        return f"page {pages[0]} is"
    else:
        return f"pages {', '.join(pages)} are"


# [END documentai_process_splitter_document]


# [START documentai_process_ocr_document]
# [START documentai_process_form_document]
# [START documentai_process_specialized_document]
# [START documentai_process_splitter_document]
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


# [END documentai_process_specialized_document]
# [END documentai_process_splitter_document]
def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )


# [END documentai_process_form_document]
# [END documentai_process_ocr_document]
