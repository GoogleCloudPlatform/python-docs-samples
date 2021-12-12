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

# [START documentai_process_form_document]

# TODO(developer): Uncomment these variables before running the sample.
# project_id= 'YOUR_PROJECT_ID'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor in Cloud Console
# file_path = '/path/to/local/pdf'


def process_document_form_sample(
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

    print("Document processing complete.")

    # Read the table and form fields output from the processor
    # The form processor also contains OCR data. For more information
    # on how to parse OCR data please see the OCR sample.
    # For a full list of Document object attributes, please reference this page: https://googleapis.dev/python/documentai/latest/_modules/google/cloud/documentai_v1beta3/types/document.html#Document
    document = result.document
    text = document.text
    print(f"Full document text: {repr(text)}\n")
    print(f"There are {len(document.pages)} page(s) in this document.")

    # Read the text recognition output from the processor
    for page in document.pages:
        print(f"\n\n**** Page {page.page_number} ****")

        print(f"Found {len(page.tables)} table(s):")
        for table in page.tables:
            num_collumns = len(table.header_rows[0].cells)
            num_rows = len(table.body_rows)
            print(f"Table with {num_collumns} columns and {num_rows} rows:")
            print_table_info(table, text)
        print(f"Found {len(page.form_fields)} form fields:")
        for field in page.form_fields:
            name = layout_to_text(field.field_name, text)
            value = layout_to_text(field.field_value, text)
            print(f"    * {repr(name.strip())}: {repr(value.strip())}")


def print_table_info(table: dict, text: str) -> None:
    # Print header row
    header_row_text = ""
    for header_cell in table.header_rows[0].cells:
        header_cell_text = layout_to_text(header_cell.layout, text)
        header_row_text += f"{repr(header_cell_text.strip())} | "
    print(f"Collumns: {header_row_text[:-3]}")
    # Print first body row
    body_row_text = ""
    for body_cell in table.body_rows[0].cells:
        body_cell_text = layout_to_text(body_cell.layout, text)
        body_row_text += f"{repr(body_cell_text.strip())} | "
    print(f"First row data: {body_row_text[:-3]}\n")


def layout_to_text(layout: dict, text: str) -> str:
    """
    Document AI identifies form fields by their offsets in the entirity of the
    document's text. This function converts offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in layout.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in layout.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response


# [END documentai_process_form_document]
