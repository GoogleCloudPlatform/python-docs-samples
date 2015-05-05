from __future__ import print_function

from samples.utils import get_service
import ast
import uuid
import json


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
        line = raw_input(
                "Enter another row into the table \n" +
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
