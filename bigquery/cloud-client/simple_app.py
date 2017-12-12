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
# [START bigquery_simple_app_deps]
from google.cloud import bigquery
# [END bigquery_simple_app_deps]


def query_stackoverflow():
    # [START create_client]
    client = bigquery.Client()
    # [END create_client]
    # [START run_query]
    query_job = client.query("""
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10""")

    results = query_job.result()  # Waits for job to complete.
    # [END run_query]

    # [START print_results]
    for row in results:
        print("{} : {} views".format(row.url, row.view_count))
    # [END print_results]


if __name__ == '__main__':
    query_stackoverflow()
# [END all]
