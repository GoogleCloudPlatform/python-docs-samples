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

"""Command-line application that loads data into BigQuery via HTTP POST.

This sample is used on this page:

    https://cloud.google.com/bigquery/loading-data-into-bigquery

For more information, see the README.rst.
"""

import argparse
import json
import time

import googleapiclient.discovery
import googleapiclient.http


# [START make_post]
def load_data(schema_path, data_path, project_id, dataset_id, table_id):
    """Loads the given data file into BigQuery.

    Args:
        schema_path: the path to a file containing a valid bigquery schema.
            see https://cloud.google.com/bigquery/docs/reference/v2/tables
        data_path: the name of the file to insert into the table.
        project_id: The project id that the table exists under. This is also
            assumed to be the project id this request is to be made under.
        dataset_id: The dataset id of the destination table.
        table_id: The table id to load data into.
    """
    # Create a bigquery service object.
    bigquery = googleapiclient.discovery.build('bigquery', 'v2')

    # Infer the data format from the name of the data file.
    source_format = 'CSV'
    if data_path[-5:].lower() == '.json':
        source_format = 'NEWLINE_DELIMITED_JSON'

    # Post to the jobs resource using the client's media upload interface. See:
    # http://developers.google.com/api-client-library/python/guide/media_upload
    insert_request = bigquery.jobs().insert(
        projectId=project_id,
        # Provide a configuration object. See:
        # https://cloud.google.com/bigquery/docs/reference/v2/jobs#resource
        body={
            'configuration': {
                'load': {
                    'schema': {
                        'fields': json.load(open(schema_path, 'r'))
                    },
                    'destinationTable': {
                        'projectId': project_id,
                        'datasetId': dataset_id,
                        'tableId': table_id
                    },
                    'sourceFormat': source_format,
                }
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(
            data_path,
            mimetype='application/octet-stream'))
    job = insert_request.execute()

    print('Waiting for job to finish...')

    status_request = bigquery.jobs().get(
        projectId=job['jobReference']['projectId'],
        jobId=job['jobReference']['jobId'])

    # Poll the job until it finishes.
    while True:
        result = status_request.execute(num_retries=2)

        if result['status']['state'] == 'DONE':
            if result['status'].get('errors'):
                raise RuntimeError('\n'.join(
                    e['message'] for e in result['status']['errors']))
            print('Job complete.')
            return

        time.sleep(1)
# [END make_post]


# [START main]
def main(project_id, dataset_id, table_name, schema_path, data_path):
    load_data(
        schema_path,
        data_path,
        project_id,
        dataset_id,
        table_name)
# [END main]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('dataset_id', help='A BigQuery dataset ID.')
    parser.add_argument(
        'table_name', help='Name of the table to load data into.')
    parser.add_argument(
        'schema_file',
        help='Path to a schema file describing the table schema.')
    parser.add_argument(
        'data_file',
        help='Path to the data file.')

    args = parser.parse_args()

    main(
        args.project_id,
        args.dataset_id,
        args.table_name,
        args.schema_file,
        args.data_file)
