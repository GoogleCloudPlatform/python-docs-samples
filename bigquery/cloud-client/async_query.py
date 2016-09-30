#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line application to perform asynchronous queries in BigQuery.

For more information, see the README.md under /bigquery.

Example invocation:
    $ python async_query.py \
          'SELECT corpus FROM `publicdata.samples.shakespeare` GROUP BY corpus'
"""

import argparse
import time
import uuid

from google.cloud import bigquery


def async_query(query):
    client = bigquery.Client()
    query_job = client.run_async_query(str(uuid.uuid4()), query)
    query_job.use_legacy_sql = False
    query_job.begin()

    wait_for_job(query_job)

    # Manually construct the QueryResults.
    # TODO: The client library will provide a helper method that does this.
    # https://github.com/GoogleCloudPlatform/gcloud-python/issues/2083
    query_results = bigquery.query.QueryResults('', client)
    query_results._properties['jobReference'] = {
        'jobId': query_job.name,
        'projectId': query_job.project
    }

    # Drain the query results by requesting a page at a time.
    page_token = None

    while True:
        rows, total_rows, page_token = query_results.fetch_data(
            max_results=10,
            page_token=page_token)

        for row in rows:
            print(row)

        if not page_token:
            break


def wait_for_job(job):
    while True:
        job.reload()  # Refreshes the state via a GET request.
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError(job.error_result)
            return
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('query', help='BigQuery SQL Query.')

    args = parser.parse_args()

    async_query(args.query)
