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


def parse_table_gcs(gcs_source_uri, gcs_destination_uri):
    from google.cloud import document
    from google.cloud.document import types

    client = document.DocumentUnderstandingServiceClient()

    # build input_config
    gcs_source_uri = 'gs://cloud-document-e2e-testing/Table1.pdf'
    gcs_source = types.GcsSource(uri=gcs_source_uri)
    input_config = types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')

    # build output_config
    pages_per_shard = 2
    gcs_destination_uri = 'gs://cloud-document-e2e-testing/yuhanliu-test/'
    gcs_destination = types.GcsDestination(uri=gcs_destination_uri)
    output_config = types.OutputConfig(gcs_destination=gcs_destination, pages_per_shard=pages_per_shard)

    # feature specific parameters
    # ...
    table_extraction_params = types.TableExtractionParams(enabled=True)

    request = types.ProcessDocumentRequest(
        input_config=input_config, output_config=output_config,
        table_extraction_params=table_extraction_params)

    requests = [request]
    operation = client.batch_process_documents(requests)

    print('Waiting for operation to finish.')
    result = operation.result(timeout=60)

    print(result)


if __name__ == '__main__':
    parse_table_gcs(None, None)