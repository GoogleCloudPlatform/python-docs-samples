#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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


"""OCR with PDF/TIFF as source files on GCS

Example:
    python docpdf.py --gcs-source-uri gs://python-docs-samples-tests/HodgeConj.pdf \
    --gcs-destination-uri gs://BUCKET_NAME/OCR/
"""

import argparse
import json
import re

from google.cloud import vision_v1p2beta1 as vision
from google.cloud import storage
from google.protobuf import json_format


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    result = operation.result(90)

    # Retrieve the first output file from GCS
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    object_name = match.group(2) + 'output-1-to-2.json'

    bucket = storage_client.get_bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name=object_name)

    # Print the full text from the first page.
    # The response additionally includes individual detected symbol's
    # confidence and bounding box.
    json_string = blob.download_as_string()
    response = json.loads(json_string)

    first_page = response['responses'][0]
    print(first_page['fullTextAnnotation']['text'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gcs-source-uri', required=True)
    parser.add_argument('--gcs-destination-uri', required=True)

    args = parser.parse_args()
    async_detect_document(args.gcs_source_uri, args.gcs_destination_uri)

