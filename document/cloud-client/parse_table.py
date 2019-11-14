#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse


# [START document_parse_table]
def parse_table_gcs(project_id, gcs_source_uri, gcs_destination_uri):
    """Parse table with PDF/TIFF as source files on Google Cloud Storage."""
    import re
    from google.cloud import documentai
    from google.cloud.documentai import types
    from google.cloud import storage
    from google.protobuf import json_format

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = types.GcsSource(uri=gcs_source_uri)
    input_config = types.InputConfig(
        gcs_source=gcs_source, mime_type='application/pdf')

    # How many pages should be grouped into each json output file.
    pages_per_shard = 1
    gcs_destination = types.GcsDestination(uri=gcs_destination_uri)
    output_config = types.OutputConfig(
        gcs_destination=gcs_destination, pages_per_shard=pages_per_shard)

    # Provide the optional table bounding box hint for
    # improved table detection accuracy.
    # The coordinates are normalized between 0 and 1.
    # The vertices here are set to work with the table in
    # gs://cloud-samples/data/documentai/fake_invoice.pdf.
    bounding_box = types.BoundingPoly(normalized_vertices=[
        types.NormalizedVertex(x=0, y=0.25),
        types.NormalizedVertex(x=1, y=0.25),
        types.NormalizedVertex(x=1, y=0.5),
        types.NormalizedVertex(x=0, y=0.5)
    ])

    # The hint is applied to all pages by default.  Optionally passing in a
    # `page_number` parameter to apply the hint to specific pages.
    table_bound_hint = types.TableBoundHint(bounding_box=bounding_box)
    table_extraction_params = types.TableExtractionParams(
        enabled=True, table_bound_hints=[table_bound_hint])

    request = types.ProcessDocumentRequest(
        input_config=input_config, output_config=output_config,
        table_extraction_params=table_extraction_params)

    requests = [request]

    print('Waiting for operation to finish.')
    parent = 'projects/{}'.format(project_id)
    operation = client.batch_process_documents(requests, parent=parent)

    _ = operation.result(timeout=60)

    # After the output json files have been written to GCS we can process them.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output.  We specified pages_per_shard=1,
    # so this corresponds to the data extracted from the first page
    # of the document.
    first_output = blob_list[0]
    json = first_output.download_as_string()

    response = json_format.Parse(
        json, types.Document(), ignore_unknown_fields=True)

    # helper function to get the extracted text from text_anchor.
    def get_text(text_anchor):
        text = ''
        for segment in text_anchor.text_segments:
            text += response.text[segment.start_index:segment.end_index]

        return text.strip()

    first_page = response.pages[0]
    first_table = first_page.tables[0]

    first_header_row = first_table.header_rows[0]
    for cell in first_header_row.cells:
        # Get the text
        text = get_text(cell.layout.text_anchor)
        print('Header row: {}'.format(text))

    for body_row in first_table.body_rows:
        print('Body row:')
        for cell in body_row.cells:
            text = get_text(cell.layout.text_anchor)
            print('Extracted cell: {}'.format(text))
# [END document_parse_table]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id')
    parser.add_argument('gcs_source_uri')
    parser.add_argument('gcs_destination_uri')
    args = parser.parse_args()

    parse_table_gcs(
        args.project_id, args.gcs_source_uri, args.gcs_destination_uri)
