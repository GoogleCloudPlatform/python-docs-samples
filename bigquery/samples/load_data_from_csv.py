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
import json
import uuid

from bigquery.samples.utils import get_service, poll_job


# [START load_table]
def load_table(service, source_schema, source_csv,
               projectId, datasetId, tableId, num_retries=5):
    """
    Starts a job to load a bigquery table from CSV

    Args:
        service: an initialized and authorized bigquery
        google-api-client object
        source_schema: a valid bigquery schema,
        see https://cloud.google.com/bigquery/docs/reference/v2/tables
        source_csv: the fully qualified Google Cloud Storage location of
        the data to load into your table

    Returns: a bigquery load job, see
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load
    """

    # Generate a unique job_id so retries
    # don't accidentally duplicate query
    job_data = {
        'jobReference': {
            'projectId': projectId,
            'job_id': str(uuid.uuid4())
        },
        'configuration': {
            'load': {
                'sourceUris': [source_csv],
                'schema': {
                    'fields': source_schema
                },
                'destinationTable': {
                    'projectId': projectId,
                    'datasetId': datasetId,
                    'tableId': tableId
                }
            }
        }
    }

    return service.jobs().insert(
        projectId=projectId,
        body=job_data).execute(num_retries=num_retries)
# [END load_table]


# [START run]
def run(source_schema, source_csv,
        projectId, datasetId, tableId, interval,  num_retries):
    service = get_service()

    job = load_table(service, source_schema, source_csv,
                     projectId, datasetId, tableId, num_retries)

    poll_job(service,
             job['jobReference']['projectId'],
             job['jobReference']['jobId'],
             interval,
             num_retries)
# [END run]


# [START main]
def main():
    projectId = raw_input("Enter the project ID: ")
    datasetId = raw_input("Enter a dataset ID: ")
    tableId = raw_input("Enter a destination table name: ")

    schema_file_path = raw_input(
        "Enter the path to the table schema: ")
    with open(schema_file_path, 'r') as schema_file:
        schema = json.load(schema_file)

    data_file_path = raw_input(
        "Enter the Cloud Storage path for the CSV file: ")
    num_retries = raw_input(
        "Enter number of times to retry in case of 500 error: ")
    interval = raw_input(
        "Enter how often to poll the query for completion (seconds): ")
    run(schema,
        data_file_path,
        projectId,
        datasetId,
        tableId,
        interval,
        num_retries)

    print("Job complete!")
# [END main]
