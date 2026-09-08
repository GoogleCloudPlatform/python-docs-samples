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

from google.cloud import bigquery


def relax_column(table_id: str) -> bigquery.Table:
    orig_table_id = table_id

    # [START bigquery_relax_column]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to full name of the table you want to create.
    table_id = "your-project.your_dataset.your_table"

    # [END bigquery_relax_column]
    table_id = orig_table_id

    # [START bigquery_relax_column]
    table = client.get_table(table_id)
    new_schema = []
    for field in table.schema:
        if field.mode != "REQUIRED":
            new_schema.append(field)
        else:
            # SchemaField properties cannot be edited after initialization.
            # To make changes, construct new SchemaField objects.
            new_field = field.to_api_repr()
            new_field["mode"] = "NULLABLE"
            relaxed_field = bigquery.SchemaField.from_api_repr(new_field)
            new_schema.append(relaxed_field)

    table.schema = new_schema
    table = client.update_table(table, ["schema"])

    print(f"Updated {table_id} schema: {table.schema}.")

    # [END bigquery_relax_column]
    return table
