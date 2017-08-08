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

"""Command-line application that demonstrates basic BigQuery API usage.

This sample queries a public shakespeare dataset and displays the 10 of
Shakespeare's works with the greatest number of distinct words.

This sample is used on this page:

    https://cloud.google.com/bigquery/bigquery-api-quickstart

For more information, see the README.rst.
"""
# [START all]
import argparse

import googleapiclient.discovery
from googleapiclient.errors import HttpError


def main(project_id):
    # [START build_service]
    # Construct the service object for interacting with the BigQuery API.
    bigquery_service = googleapiclient.discovery.build('bigquery', 'v2')
    # [END build_service]

    try:
        # [START run_query]
        query_request = bigquery_service.jobs()
        query_data = {
            'query': (
                'SELECT TOP(corpus, 10) as title, '
                'COUNT(*) as unique_words '
                'FROM [publicdata:samples.shakespeare];')
        }

        query_response = query_request.query(
            projectId=project_id,
            body=query_data).execute()
        # [END run_query]

        # [START print_results]
        print('Query Results:')
        for row in query_response['rows']:
            print('\t'.join(field['v'] for field in row['f']))
        # [END print_results]

    except HttpError as err:
        print('Error: {}'.format(err.content))
        raise err


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')

    args = parser.parse_args()

    main(args.project_id)
# [END all]
