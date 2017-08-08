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

For more information, see the README.rst.
"""

import argparse
import json

import googleapiclient.discovery


# [START sync_query]
def sync_query(
        bigquery, project_id, query,
        timeout=10000, num_retries=5, use_legacy_sql=False):
    query_data = {
        'query': query,
        'timeoutMs': timeout,
        # Set to False to use standard SQL syntax. See:
        # https://cloud.google.com/bigquery/sql-reference/enabling-standard-sql
        'useLegacySql': use_legacy_sql
    }
    return bigquery.jobs().query(
        projectId=project_id,
        body=query_data).execute(num_retries=num_retries)
# [END sync_query]


# [START run]
def main(project_id, query, timeout, num_retries, use_legacy_sql):
    # [START build_service]
    # Construct the service object for interacting with the BigQuery API.
    bigquery = googleapiclient.discovery.build('bigquery', 'v2')
    # [END build_service]

    query_job = sync_query(
        bigquery,
        project_id,
        query,
        timeout,
        num_retries,
        use_legacy_sql)

    # [START paging]
    # Page through the result set and print all results.
    results = []
    page_token = None

    while True:
        page = bigquery.jobs().getQueryResults(
            pageToken=page_token,
            **query_job['jobReference']).execute(num_retries=2)

        results.extend(page.get('rows', []))

        page_token = page.get('pageToken')
        if not page_token:
            break

    print(json.dumps(results))
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
    parser.add_argument(
        '-l', '--use_legacy_sql',
        help='Use legacy BigQuery SQL syntax instead of standard SQL syntax.',
        type=bool,
        default=False)

    args = parser.parse_args()

    main(
        args.project_id,
        args.query,
        args.timeout,
        args.num_retries,
        args.use_legacy_sql)

# [END main]
