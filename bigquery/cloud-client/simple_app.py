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
import uuid

from google.cloud import bigquery


def query_shakespeare():
    client = bigquery.Client()
    # [END create_client]
    # [START run_query]
    query_job = client.run_async_query(str(uuid.uuid4()), """
        #standardSQL
        SELECT corpus AS title, COUNT(*) AS unique_words
        FROM `publicdata.samples.shakespeare`
        GROUP BY title
        ORDER BY unique_words DESC
        LIMIT 10""")

    query_job.begin()
    query_job.result()  # Wait for job to complete.
    # [END run_query]

    # [START print_results]
    destination_table = query_job.destination
    destination_table.reload()
    for row in destination_table.fetch_data():
        print(row)
    # [END print_results]


if __name__ == '__main__':
    query_shakespeare()
# [END all]
