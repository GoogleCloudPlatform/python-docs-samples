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
import argparse
import uuid

from .utils import get_service, poll_job


# [START export_table]
def export_table(service, cloud_storage_path,
                 project_id, dataset_id, table_id,
                 export_format="CSV",
                 num_retries=5):
    """
    Starts an export job

    Args:
        service: initialized and authorized bigquery
            google-api-client object.
        cloud_storage_path: fully qualified
            path to a Google Cloud Storage location.
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
            'projectId': project_id,
            'jobId': str(uuid.uuid4())
        },
        'configuration': {
            'extract': {
                'sourceTable': {
                    'projectId': project_id,
                    'datasetId': dataset_id,
                    'tableId': table_id,
                },
                'destinationUris': [cloud_storage_path],
                'destinationFormat': export_format
            }
        }
    }
    return service.jobs().insert(
        projectId=project_id,
        body=job_data).execute(num_retries=num_retries)
# [END export_table]


# [START run]
def main(cloud_storage_path, project_id, dataset_id, table_id,
         num_retries, interval, export_format="CSV"):

    bigquery = get_service()
    resource = export_table(bigquery, cloud_storage_path,
                            project_id, dataset_id, table_id,
                            num_retries=num_retries,
                            export_format=export_format)
    poll_job(bigquery,
             resource['jobReference']['projectId'],
             resource['jobReference']['jobId'],
             interval,
             num_retries)
# [END run]


# [START main]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Exports data from BigQuery to Google Cloud Storage.')
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('dataset_id', help='BigQuery dataset to export.')
    parser.add_argument('table_id', help='BigQuery table to export.')
    parser.add_argument(
        'gcs_path',
        help=('Google Cloud Storage path to store the exported data. For '
              'example, gs://mybucket/mydata.csv'))
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
        args.gcs_path,
        args.project_id,
        args.dataset_id,
        args.table_id,
        args.num_retries,
        args.poll_interval)
# [END main]
