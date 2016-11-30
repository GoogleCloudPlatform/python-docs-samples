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

"""Loads data into BigQuery from a local file.

For more information, see the README.md under /bigquery.

Example invocation:
    $ python load_data_from_file.py example_dataset example_table \
        example-data.csv

The dataset and table should already exist.
"""

import argparse
import time

from google.cloud import bigquery


def load_data_from_file(dataset_name, table_name, source_file_name):
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)

    # Reload the table to get the schema.
    table.reload()

    with open(source_file_name, 'rb') as source_file:
        # This example uses CSV, but you can use other formats.
        # See https://cloud.google.com/bigquery/loading-data
        job = table.upload_from_file(
            source_file, source_format='text/csv')

    wait_for_job(job)

    print('Loaded {} rows into {}:{}.'.format(
        job.output_rows, dataset_name, table_name))


def wait_for_job(job):
    while True:
        job.reload()
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError(job.errors)
            return
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_name')
    parser.add_argument('table_name')
    parser.add_argument(
        'source_file_name', help='Path to a .csv file to upload.')

    args = parser.parse_args()

    load_data_from_file(
        args.dataset_name,
        args.table_name,
        args.source_file_name)
