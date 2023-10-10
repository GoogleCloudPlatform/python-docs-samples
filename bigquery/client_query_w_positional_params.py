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


def client_query_w_positional_params() -> None:
    # [START bigquery_query_params_positional]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    query = """
        SELECT word, word_count
        FROM `bigquery-public-data.samples.shakespeare`
        WHERE corpus = ?
        AND word_count >= ?
        ORDER BY word_count DESC;
    """
    # Set the name to None to use positional parameters.
    # Note that you cannot mix named and positional parameters.
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(None, "STRING", "romeoandjuliet"),
            bigquery.ScalarQueryParameter(None, "INT64", 250),
        ]
    )
    query_job = client.query(query, job_config=job_config)  # Make an API request.

    for row in query_job:
        print("{}: \t{}".format(row.word, row.word_count))
    # [END bigquery_query_params_positional]
