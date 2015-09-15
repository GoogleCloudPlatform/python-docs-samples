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
#
import argparse
import ast
import json
import uuid

from six.moves import input
from .utils import get_service


# [START stream_row_to_bigquery]
def stream_row_to_bigquery(service, project_id, dataset_id, table_name, row,
                           num_retries=5):
    # Generate a unique row id so retries
    # don't accidentally duplicate insert
    insert_all_data = {
        'insertId': str(uuid.uuid4()),
        'rows': [{'json': row}]
    }
    return service.tabledata().insertAll(
        projectId=project_id,
        datasetId=dataset_id,
        tableId=table_name,
        body=insert_all_data).execute(num_retries=num_retries)
    # [END stream_row_to_bigquery]


# [START run]
def main(project_id, dataset_id, table_name, num_retries):
    service = get_service()
    for row in get_rows():
        response = stream_row_to_bigquery(
            service, project_id, dataset_id, table_name, row, num_retries)
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
        description='Streams data into BigQuery from the command line.')
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
