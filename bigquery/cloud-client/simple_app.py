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

"""Simple application that performs a query with BigQuery."""
# [START all]
# [START create_client]
from google.cloud import bigquery


def query_shakespeare():
    client = bigquery.Client()
    # [END create_client]
    # [START run_query]
    query_results = client.run_sync_query("""
        SELECT
            APPROX_TOP_COUNT(corpus, 10) as title,
            COUNT(*) as unique_words
        FROM `publicdata.samples.shakespeare`;""")

    # Use standard SQL syntax for queries.
    # See: https://cloud.google.com/bigquery/sql-reference/
    query_results.use_legacy_sql = False

    query_results.run()
    # [END run_query]

    # [START print_results]
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
    # [END print_results]


if __name__ == '__main__':
    query_shakespeare()
# [END all]
