#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Exports data from BigQuery to an object in Google Cloud Storage.

For more information, see the README.rst.

Example invocation:
    $ python export_data_to_gcs.py example_dataset example_table \\
        gs://example-bucket/example-data.csv

The dataset and table should already exist.
"""

import argparse

from google.cloud import bigquery


def export_data_to_gcs(dataset_id, table_id, destination):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    job = bigquery_client.extract_table(table_ref, destination)

    job.result()  # Waits for job to complete

    print('Exported {}:{} to {}'.format(
        dataset_id, table_id, destination))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_id')
    parser.add_argument('table_id')
    parser.add_argument(
        'destination', help='The destination Google Cloud Storage object. '
        'Must be in the format gs://bucket_name/object_name')

    args = parser.parse_args()

    export_data_to_gcs(
        args.dataset_id,
        args.table_id,
        args.destination)
