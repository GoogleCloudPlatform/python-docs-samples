# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def client_query_dry_run() -> "bigquery.QueryJob":
    # [START bigquery_query_dry_run]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        (
            "SELECT name, COUNT(*) as name_count "
            "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
            "WHERE state = 'WA' "
            "GROUP BY name"
        ),
        job_config=job_config,
    )  # Make an API request.

    # A dry run query completes immediately.
    print("This query will process {} bytes.".format(query_job.total_bytes_processed))
    # [END bigquery_query_dry_run]
    return query_job
