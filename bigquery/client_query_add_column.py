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


def client_query_add_column(table_id: str) -> None:
    # [START bigquery_add_column_query_append]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the destination table.
    # table_id = "your-project.your_dataset.your_table_name"

    # Retrieves the destination table and checks the length of the schema.
    table = client.get_table(table_id)  # Make an API request.
    print("Table {} contains {} columns".format(table_id, len(table.schema)))

    # Configures the query to append the results to a destination table,
    # allowing field addition.
    job_config = bigquery.QueryJobConfig(
        destination=table_id,
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    # Start the query, passing in the extra configuration.
    client.query_and_wait(
        # In this example, the existing table contains only the 'full_name' and
        # 'age' columns, while the results of this query will contain an
        # additional 'favorite_color' column.
        'SELECT "Timmy" as full_name, 85 as age, "Blue" as favorite_color;',
        job_config=job_config,
    )  # Make an API request and wait for job to complete.

    # Checks the updated length of the schema.
    table = client.get_table(table_id)  # Make an API request.
    print("Table {} now contains {} columns".format(table_id, len(table.schema)))
    # [END bigquery_add_column_query_append]
