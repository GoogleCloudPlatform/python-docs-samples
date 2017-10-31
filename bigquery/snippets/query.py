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

"""Command-line application to perform queries in BigQuery.

For more information, see the README.rst.

Example invocation:
    $ python query.py '#standardSQL
          SELECT corpus
          FROM `bigquery-public-data.samples.shakespeare`
          GROUP BY corpus
          ORDER BY corpus'
"""

import argparse

from google.cloud import bigquery


def query(query):
    client = bigquery.Client()
    query_job = client.query(query)

    # Print the results.
    for row in query_job.result():  # Waits for job to complete.
        print(row)


def query_standard_sql(query):
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig()

    # Set use_legacy_sql to False to use standard SQL syntax.
    # Note that queries are treated as standard SQL by default.
    job_config.use_legacy_sql = False
    query_job = client.query(query, job_config=job_config)

    # Print the results.
    for row in query_job.result():  # Waits for job to complete.
        print(row)


def query_destination_table(query, dest_dataset_id, dest_table_id):
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig()

    # Allow for query results larger than the maximum response size.
    job_config.allow_large_results = True

    # When large results are allowed, a destination table must be set.
    dest_dataset_ref = client.dataset(dest_dataset_id)
    dest_table_ref = dest_dataset_ref.table(dest_table_id)
    job_config.destination = dest_table_ref

    # Allow the results table to be overwritten.
    job_config.write_disposition = 'WRITE_TRUNCATE'

    query_job = client.query(query, job_config=job_config)

    # Print the results.
    for row in query_job.result():  # Waits for job to complete.
        print(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('query', help='BigQuery SQL Query.')
    parser.add_argument(
        '--use_standard_sql',
        action='store_true',
        help='Use standard SQL syntax.')
    parser.add_argument(
        '--destination_table',
        type=str,
        help=(
            'Destination table to use for results. '
            'Example: my_dataset.my_table'))

    args = parser.parse_args()

    if args.use_standard_sql:
        query_standard_sql(args.query)
    elif args.destination_table:
        dataset, table = args.destination_table.split('.')
        query_destination_table(args.query, dataset, table)
    else:
        query(args.query)
