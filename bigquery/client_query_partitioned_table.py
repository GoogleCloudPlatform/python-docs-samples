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


def client_query_partitioned_table(client, table_id):

    # [START bigquery_query_partitioned_table]
    import datetime

    from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to query from.
    # table_id = "your-project.your_dataset.your_table_name"

    sql = """
        SELECT *
        FROM `{}`
        WHERE date BETWEEN @start_date AND @end_date
    """.format(
        table_id
    )

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "start_date", "DATE", datetime.date(1800, 1, 1)
            ),
            bigquery.ScalarQueryParameter(
                "end_date", "DATE", datetime.date(1899, 12, 31)
            ),
        ]
    )
    query_job = client.query(sql, job_config=job_config)  # Make an API request.

    rows = list(query_job)
    print("{} states were admitted to the US in the 1800s".format(len(rows)))
    # [END bigquery_query_partitioned_table]
