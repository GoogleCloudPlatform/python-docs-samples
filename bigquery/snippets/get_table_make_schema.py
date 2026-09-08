# Copyright 2022 Google LLC
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


def get_table_make_schema(table_id: str, schema_path: str) -> None:
    orig_table_id = table_id
    orig_schema_path = schema_path
    # [START bigquery_schema_file_get]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change the table_id variable to the full name of the
    # table you want to get schema from.
    table_id = "your-project.your_dataset.your_table_name"

    # TODO(dev): Change schema_path variable to the path
    # of your schema file.
    schema_path = "path/to/schema.json"
    # [END bigquery_schema_file_get]
    table_id = orig_table_id
    schema_path = orig_schema_path
    # [START bigquery_schema_file_get]
    table = client.get_table(table_id)  # Make an API request.

    # Write a schema file to schema_path with the schema_to_json method.
    client.schema_to_json(table.schema, schema_path)

    with open(schema_path, "r", encoding="utf-8") as schema_file:
        schema_contents = schema_file.read()

    # View table properties
    print(f"Got table '{table.project}.{table.dataset_id}.{table.table_id}'.")
    print(f"Table schema: {schema_contents}")

    # [END bigquery_schema_file_get]
