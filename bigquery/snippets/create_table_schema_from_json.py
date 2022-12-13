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

import pathlib


def create_table(table_id: str) -> None:
    orig_table_id = table_id
    current_directory = pathlib.Path(__file__).parent
    orig_schema_path = str(current_directory / "schema.json")
    # [START bigquery_schema_file_create]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you want to create.
    table_id = "your-project.your_dataset.your_table_name"
    # TODO(dev): Change schema_path variable to the path of your schema file.
    schema_path = "path/to/schema.json"
    # [END bigquery_schema_file_create]
    table_id = orig_table_id
    schema_path = orig_schema_path

    # [START bigquery_schema_file_create]
    # To load a schema file use the schema_from_json method.
    schema = client.schema_from_json(schema_path)

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # API request
    print(f"Created table {table_id}.")
    # [END bigquery_schema_file_create]
