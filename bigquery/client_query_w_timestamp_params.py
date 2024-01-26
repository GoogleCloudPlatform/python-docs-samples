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


def client_query_w_timestamp_params() -> None:
    # [START bigquery_query_params_timestamps]
    import datetime

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    query = "SELECT TIMESTAMP_ADD(@ts_value, INTERVAL 1 HOUR);"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "ts_value",
                "TIMESTAMP",
                datetime.datetime(2016, 12, 7, 8, 0, tzinfo=datetime.timezone.utc),
            )
        ]
    )
    results = client.query_and_wait(
        query, job_config=job_config
    )  # Make an API request.

    for row in results:
        print(row)
    # [END bigquery_query_params_timestamps]
