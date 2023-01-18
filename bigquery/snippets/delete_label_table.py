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


def delete_label_table(table_id: str, label_key: str) -> bigquery.Table:
    orig_table_id = table_id
    orig_label_key = label_key
    # [START bigquery_delete_label_table]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you wish to delete from.
    table_id = "your-project.your_dataset.your_table_name"
    # TODO(dev): Change label_key to the name of the label you want to remove.
    label_key = "color"
    # [END bigquery_delete_label_table]
    table_id = orig_table_id
    label_key = orig_label_key
    # [START bigquery_delete_label_table]
    table = client.get_table(table_id)  # API request

    # To delete a label from a table, set its value to None
    table.labels[label_key] = None

    table = client.update_table(table, ["labels"])  # API request

    print(f"Deleted label '{label_key}' from {table_id}.")
    # [END bigquery_delete_label_table]
    return table
