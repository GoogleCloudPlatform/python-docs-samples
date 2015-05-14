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
from __future__ import print_function

import ast
import json
import uuid

from bigquery.samples.utils import get_service


# [START stream_row_to_bigquery]
def stream_row_to_bigquery(service,
                           project_id,
                           dataset_id,
                           table_id,
                           row,
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
        tableId=table_id,
        body=insert_all_data).execute(num_retries=num_retries)
    # [END stream_row_to_bigquery]


# [START run]
def run(project_id, dataset_id, table_id, rows, num_retries):
    service = get_service()
    for row in rows:
        response = stream_row_to_bigquery(service,
                                          project_id,
                                          dataset_id,
                                          table_id,
                                          row,
                                          num_retries)
        yield json.dumps(response)
# [END run]


# [START main]
def get_rows():
    line = raw_input("Enter a row (python dict) into the table: ")
    while line:
        yield ast.literal_eval(line)
        line = raw_input("Enter another row into the table \n" +
                         "[hit enter to stop]: ")


def main():
    project_id = raw_input("Enter the project ID: ")
    dataset_id = raw_input("Enter a dataset ID: ")
    table_id = raw_input("Enter a table ID : ")
    num_retries = int(raw_input(
        "Enter number of times to retry in case of 500 error: "))

    for result in run(project_id, dataset_id, table_id,
                      get_rows(), num_retries):
        print(result)
# [END main]
