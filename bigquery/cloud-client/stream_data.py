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

"""Loads a single row of data directly into BigQuery.

For more information, see the README.md under /bigquery.

Example invocation:
    $ python stream_data.py example_dataset example_table \
        '["Gandalf", 2000]'

The dataset and table should already exist.
"""

import argparse
import json
from pprint import pprint

from google.cloud import bigquery


def stream_data(dataset_name, table_name, json_data):
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)
    data = json.loads(json_data)

    # Reload the table to get the schema.
    table.reload()

    rows = [data]
    errors = table.insert_data(rows)

    if not errors:
        print('Loaded 1 row into {}:{}'.format(dataset_name, table_name))
    else:
        print('Errors:')
        pprint(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_name')
    parser.add_argument('table_name')
    parser.add_argument(
        'json_data',
        help='The row to load into BigQuery as an array in JSON format.')

    args = parser.parse_args()

    stream_data(
        args.dataset_name,
        args.table_name,
        args.json_data)
