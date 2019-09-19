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


# [START document_parse_table]
def parse_table_gcs(gcs_source_uri, gcs_destination_uri):
    """Parse table with PDF/TIFF as source files on Google Cloud Storage."""
    import re
    from google.cloud import document
    from google.cloud.document import types
    from google.cloud import storage
    from google.protobuf import json_format

    client = document.DocumentUnderstandingServiceClient()

    gcs_source = types.GcsSource(uri=gcs_source_uri)
    input_config = types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')

    # How many pages should be grouped into each json output file.
    pages_per_shard = 1
    gcs_destination = types.GcsDestination(uri=gcs_destination_uri)
    output_config = types.OutputConfig(gcs_destination=gcs_destination, pages_per_shard=pages_per_shard)

    # Provide the optional table bounding box hint for improved table detection accuracy.
    # The coordinates are normalized between 0 and 1.
    bounding_box = types.BoundingPoly(normalized_vertices=[
        types.NormalizedVertex(x=0, y=0),
        types.NormalizedVertex(x=1, y=0),
        types.NormalizedVertex(x=1, y=1),
        types.NormalizedVertex(x=0, y=1)
    ])

    # The hint is applied to all pages by default.  Optionally passing in a `page_number` parameter to apply the hint to specific pages.
    table_bound_hint = types.TableBoundHint(bounding_box=bounding_box)
    table_extraction_params = types.TableExtractionParams(enabled=True, table_bound_hints=[table_bound_hint])

    request = types.ProcessDocumentRequest(
        input_config=input_config, output_config=output_config,
        table_extraction_params=table_extraction_params)

    requests = [request]

    print('Waiting for operation to finish.')
    operation = client.batch_process_documents(requests)

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

    # Process the first output.  We specified pages_per_shard=1, so this corresponds to the first page.
    first_output = blob_list[0]
    json = first_output.download_as_string()

    response = json_format.Parse(json, types.Document(), ignore_unknown_fields=True)




# [END document_parse_table]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('gcs_source_uri')
    parser.add_argument('gcs_destination_uri')
    args = parser.parse_args()

    parse_table_gcs(args.gcs_source_uri, args.gcs_destination_uri)