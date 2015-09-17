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

"""Command-line application to perform an synchronous query in BigQuery.

This sample is used on this page:

    https://cloud.google.com/bigquery/querying-data#syncqueries

For more information, see the README.md under /bigquery.
"""

import argparse
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


# [START sync_query]
def sync_query(bigquery, project_id, query, timeout=10000, num_retries=5):
    query_data = {
        'query': query,
        'timeoutMs': timeout,
    }
    return bigquery.jobs().query(
        projectId=project_id,
        body=query_data).execute(num_retries=num_retries)
# [END sync_query]


# [START run]
def main(project_id, query, timeout, num_retries):
    # [START build_service]
    # Grab the application's default credentials from the environment.
    credentials = GoogleCredentials.get_application_default()

    # Construct the service object for interacting with the BigQuery API.
    bigquery = discovery.build('bigquery', 'v2', credentials=credentials)
    # [END build_service]

    query_job = sync_query(
        bigquery,
        project_id,
        query,
        timeout,
        num_retries)

    # [START paging]
    # Page through the result set and print all results.
    page_token = None
    while True:
        page = bigquery.jobs().getQueryResults(
            pageToken=page_token,
            **query_job['jobReference']).execute(num_retries=2)

        print(json.dumps(page['rows']))

        page_token = page.get('pageToken')
        if not page_token:
            break
    # [END paging]
# [END run]


# [START main]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('query', help='BigQuery SQL Query.')
    parser.add_argument(
        '-t', '--timeout',
        help='Number seconds to wait for a result',
        type=int,
        default=30)
    parser.add_argument(
        '-r', '--num_retries',
        help='Number of times to retry in case of 500 error.',
        type=int,
        default=5)

    args = parser.parse_args()

    main(
        args.project_id,
        args.query,
        args.timeout,
        args.num_retries)

# [END main]
