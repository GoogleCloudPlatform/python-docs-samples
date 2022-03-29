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


def add_empty_column(table_id: str) -> None:

    # [START bigquery_add_empty_column]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table
    #                  to add an empty column.
    # table_id = "your-project.your_dataset.your_table_name"

    table = client.get_table(table_id)  # Make an API request.

    original_schema = table.schema
    new_schema = original_schema[:]  # Creates a copy of the schema.
    new_schema.append(bigquery.SchemaField("phone", "STRING"))

    table.schema = new_schema
    table = client.update_table(table, ["schema"])  # Make an API request.

    if len(table.schema) == len(original_schema) + 1 == len(new_schema):
        print("A new column has been added.")
    else:
        print("The column has not been added.")
    # [END bigquery_add_empty_column]
