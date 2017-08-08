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
    $ python export_data_to_gcs.py example_dataset example_table \
        gs://example-bucket/example-data.csv

The dataset and table should already exist.
"""

import argparse
import uuid

from google.cloud import bigquery


def export_data_to_gcs(dataset_name, table_name, destination):
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)
    job_name = str(uuid.uuid4())

    job = bigquery_client.extract_table_to_storage(
        job_name, table, destination)

    job.begin()
    job.result()  # Wait for job to complete

    print('Exported {}:{} to {}'.format(
        dataset_name, table_name, destination))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_name')
    parser.add_argument('table_name')
    parser.add_argument(
        'destination', help='The desintation Google Cloud Storage object.'
        'Must be in the format gs://bucket_name/object_name')

    args = parser.parse_args()

    export_data_to_gcs(
        args.dataset_name,
        args.table_name,
        args.destination)
