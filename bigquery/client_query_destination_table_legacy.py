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


def client_query_destination_table_legacy(table_id: str) -> None:
    # [START bigquery_query_legacy_large_results]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the destination table.
    # table_id = "your-project.your_dataset.your_table_name"

    # Set the destination table and use_legacy_sql to True to use
    # legacy SQL syntax.
    job_config = bigquery.QueryJobConfig(
        allow_large_results=True, destination=table_id, use_legacy_sql=True
    )

    sql = """
        SELECT corpus
        FROM [bigquery-public-data:samples.shakespeare]
        GROUP BY corpus;
    """

    # Start the query, passing in the extra configuration.
    client.query_and_wait(
        sql, job_config=job_config
    )  # Make an API request and wait for the query to finish.

    print("Query results loaded to the table {}".format(table_id))
    # [END bigquery_query_legacy_large_results]
