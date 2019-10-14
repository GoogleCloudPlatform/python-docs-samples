#!/usr/bin/env python

# Copyright 2019 Google LLC. All Rights Reserved.
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


# [START document_parse_key_value]
def parse_key_value_gcs(project_id, gcs_source_uri, gcs_destination_uri):
    """Parse key-value pairs with PDF/TIFF as source files on Google Cloud Storage."""
    import re
    from google.cloud import documentai
    from google.cloud.documentai import types
    from google.cloud import storage
    from google.protobuf import json_format

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = types.GcsSource(uri=gcs_source_uri)
    input_config = types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')

    # How many pages should be grouped into each json output file.
    pages_per_shard = 1
    gcs_destination = types.GcsDestination(uri=gcs_destination_uri)
    output_config = types.OutputConfig(gcs_destination=gcs_destination, pages_per_shard=pages_per_shard)

    # Provide key-value pair hints.
    # For each key hint, key is some text that is likely to appear in the
    # document as key, value types are optional, but can be one or more of DATE,
    # LOCATION, ORGANIZATION, etc.
    # Accepted value types: ADDRESS, LOCATION, ORGANIZATION, PERSON, PHONE_NUMBER, ID, NUMBER, EMAIL, PRICE, TERMS, DATE, NAME
    key_value_pair_hints = [
        types.KeyValuePairHint(key='Phone', value_types=['PHONE_NUMBER']),
        types.KeyValuePairHint(key='Contact', value_types=['EMAIL', 'NAME'])
    ]

    form_extraction_params = types.FormExtractionParams(enabled=True, key_value_pair_hints=key_value_pair_hints)

    request = types.ProcessDocumentRequest(
        input_config=input_config, output_config=output_config,
        form_extraction_params=form_extraction_params)

    requests = [request]

    print('Waiting for operation to finish.')
    parent = 'projects/{}'.format(project_id)
    operation = client.batch_process_documents(requests, parent=parent)

    result = operation.result(timeout=60)

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

    # Process the first output.  We specified pages_per_shard=1, so this corresponds to the data extracted from the first first page of the document.
    first_output = blob_list[0]
    json = first_output.download_as_string()

    response = json_format.Parse(json, types.Document(), ignore_unknown_fields=True)

    def get_text(text_anchor):
        text = ''
        for segment in text_anchor.text_segments:
            text += response.text[segment.start_index:segment.end_index]

        return text.strip()

    first_page = response.pages[0]

    for field in first_page.form_fields:
        field_name_text = get_text(field.field_name.text_anchor)
        field_value_text = get_text(field.field_value.text_anchor)

        print('Extracted key-value pair: ({}, {})'.format(field_name_text, field_value_text))
# [END document_parse_key_value]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id')
    parser.add_argument('gcs_source_uri')
    parser.add_argument('gcs_destination_uri')
    args = parser.parse_args()

    parse_key_value_gcs(args.project_id, args.gcs_source_uri, args.gcs_destination_uri)