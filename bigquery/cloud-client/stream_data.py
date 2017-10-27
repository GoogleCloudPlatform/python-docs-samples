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

For more information, see the README.rst.

Example invocation:
    $ python stream_data.py example_dataset example_table \\
        '["Gandalf", 2000]'

The dataset and table should already exist.
"""

import argparse
import json
from pprint import pprint

from google.cloud import bigquery


def stream_data(dataset_id, table_id, json_data):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    data = json.loads(json_data)

    # Get the table from the API so that the schema is available.
    table = bigquery_client.get_table(table_ref)

    rows = [data]
    errors = bigquery_client.create_rows(table, rows)

    if not errors:
        print('Loaded 1 row into {}:{}'.format(dataset_id, table_id))
    else:
        print('Errors:')
        pprint(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dataset_id')
    parser.add_argument('table_id')
    parser.add_argument(
        'json_data',
        help='The row to load into BigQuery as an array in JSON format.')

    args = parser.parse_args()

    stream_data(
        args.dataset_id,
        args.table_id,
        args.json_data)
