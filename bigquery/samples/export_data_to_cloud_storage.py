#   Copyright 2015, Google, Inc.
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
import uuid

from bigquery.samples.utils import get_service
from bigquery.samples.utils import poll_job


# [START export_table]
def export_table(service, cloud_storage_path,
                 projectId, datasetId, tableId,
                 export_format="CSV",
                 num_retries=5):
    """
    Starts an export job

    Args:
        service: initialized and authorized bigquery
        google-api-client object,
        cloud_storage_path: fully qualified
        path to a Google Cloud Storage location,
        e.g. gs://mybucket/myfolder/
        export_format: format to export in;
        "CSV", "NEWLINE_DELIMITED_JSON", or "AVRO".

    Returns: an extract job resource representing the
    job, see https://cloud.google.com/bigquery/docs/reference/v2/jobs
    """
    # Generate a unique job_id so retries
    # don't accidentally duplicate export
    job_data = {
        'jobReference': {
            'projectId': projectId,
            'jobId': str(uuid.uuid4())
        },
        'configuration': {
            'extract': {
                'sourceTable': {
                    'projectId': projectId,
                    'datasetId': datasetId,
                    'tableId': tableId,
                },
                'destinationUris': [cloud_storage_path],
                'destinationFormat': export_format
            }
        }
    }
    return service.jobs().insert(
        projectId=projectId,
        body=job_data).execute(num_retries=num_retries)
# [END export_table]


# [START run]
def run(cloud_storage_path,
        projectId, datasetId, tableId,
        num_retries, interval):

    bigquery = get_service()
    resource = export_table(bigquery, cloud_storage_path,
                            projectId, datasetId, tableId, num_retries)
    poll_job(bigquery,
             resource['jobReference']['projectId'],
             resource['jobReference']['jobId'],
             interval,
             num_retries)
# [END run]


# [START main]
def main():
    projectId = raw_input("Enter the project ID: ")
    datasetId = raw_input("Enter a dataset ID: ")
    tableId = raw_input("Enter a table name to copy: ")
    cloud_storage_path = raw_input(
        "Enter a Google Cloud Storage URI: ")
    interval = raw_input(
        "Enter how often to poll the job (in seconds): ")
    num_retries = raw_input(
        "Enter the number of retries in case of 500 error: ")

    run(cloud_storage_path,
        projectId, datasetId, tableId,
        num_retries, interval)

    print 'Done exporting!'
# [END main]
