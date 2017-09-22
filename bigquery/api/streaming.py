#!/usr/bin/env python

# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line application that streams data into BigQuery.

This sample is used on this page:

    https://cloud.google.com/bigquery/streaming-data-into-bigquery

For more information, see the README.rst.
"""

import argparse
import ast
import json
import uuid

import googleapiclient.discovery
from six.moves import input


# [START stream_row_to_bigquery]
def stream_row_to_bigquery(bigquery, project_id, dataset_id, table_name, row,
                           num_retries=5):
    insert_all_data = {
        'rows': [{
            'json': row,
            # Generate a unique id for each row so retries don't accidentally
            # duplicate insert
            'insertId': str(uuid.uuid4()),
        }]
    }
    return bigquery.tabledata().insertAll(
        projectId=project_id,
        datasetId=dataset_id,
        tableId=table_name,
        body=insert_all_data).execute(num_retries=num_retries)
    # [END stream_row_to_bigquery]


# [START run]
def main(project_id, dataset_id, table_name, num_retries):
    # [START build_service]
    # Construct the service object for interacting with the BigQuery API.
    bigquery = googleapiclient.discovery.build('bigquery', 'v2')
    # [END build_service]

    for row in get_rows():
        response = stream_row_to_bigquery(
            bigquery, project_id, dataset_id, table_name, row, num_retries)
        print(json.dumps(response))


def get_rows():
    line = input("Enter a row (python dict) into the table: ")
    while line:
        yield ast.literal_eval(line)
        line = input("Enter another row into the table \n" +
                     "[hit enter to stop]: ")
# [END run]


# [START main]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('dataset_id', help='A BigQuery dataset ID.')
    parser.add_argument(
        'table_name', help='Name of the table to load data into.')
    parser.add_argument(
        '-p', '--poll_interval',
        help='How often to poll the query for completion (seconds).',
        type=int,
        default=1)
    parser.add_argument(
        '-r', '--num_retries',
        help='Number of times to retry in case of 500 error.',
        type=int,
        default=5)

    args = parser.parse_args()

    main(
        args.project_id,
        args.dataset_id,
        args.table_name,
        args.num_retries)
# [END main]
