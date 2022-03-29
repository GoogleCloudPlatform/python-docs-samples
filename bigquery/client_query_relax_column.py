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


def client_query_relax_column(table_id: str) -> None:

    # [START bigquery_relax_column_query_append]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the destination table.
    # table_id = "your-project.your_dataset.your_table_name"

    # Retrieves the destination table and checks the number of required fields.
    table = client.get_table(table_id)  # Make an API request.
    original_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)

    # In this example, the existing table has 2 required fields.
    print("{} fields in the schema are required.".format(original_required_fields))

    # Configures the query to append the results to a destination table,
    # allowing field relaxation.
    job_config = bigquery.QueryJobConfig(
        destination=table_id,
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        # In this example, the existing table contains 'full_name' and 'age' as
        # required columns, but the query results will omit the second column.
        'SELECT "Beyonce" as full_name;',
        job_config=job_config,
    )  # Make an API request.
    query_job.result()  # Wait for the job to complete.

    # Checks the updated number of required fields.
    table = client.get_table(table_id)  # Make an API request.
    current_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    print("{} fields in the schema are now required.".format(current_required_fields))
    # [END bigquery_relax_column_query_append]
