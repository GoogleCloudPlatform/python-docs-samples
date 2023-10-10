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


def query_pagination() -> None:
    # [START bigquery_query_pagination]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    query = """
        SELECT name, SUM(number) as total_people
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        GROUP BY name
        ORDER BY total_people DESC
    """
    query_job = client.query(query)  # Make an API request.
    query_job.result()  # Wait for the query to complete.

    # Get the destination table for the query results.
    #
    # All queries write to a destination table. If a destination table is not
    # specified, the BigQuery populates it with a reference to a temporary
    # anonymous table after the query completes.
    destination = query_job.destination

    # Get the schema (and other properties) for the destination table.
    #
    # A schema is useful for converting from BigQuery types to Python types.
    destination = client.get_table(destination)

    # Download rows.
    #
    # The client library automatically handles pagination.
    print("The query data:")
    rows = client.list_rows(destination, max_results=20)
    for row in rows:
        print("name={}, count={}".format(row["name"], row["total_people"]))
    # [END bigquery_query_pagination]
