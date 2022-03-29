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


def client_query_w_array_params() -> None:

    # [START bigquery_query_params_arrays]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    query = """
        SELECT name, sum(number) as count
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE gender = @gender
        AND state IN UNNEST(@states)
        GROUP BY name
        ORDER BY count DESC
        LIMIT 10;
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("gender", "STRING", "M"),
            bigquery.ArrayQueryParameter("states", "STRING", ["WA", "WI", "WV", "WY"]),
        ]
    )
    query_job = client.query(query, job_config=job_config)  # Make an API request.

    for row in query_job:
        print("{}: \t{}".format(row.name, row.count))
    # [END bigquery_query_params_arrays]
