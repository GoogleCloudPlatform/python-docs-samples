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


def label_table(table_id: str) -> None:
    orig_table_id = table_id
    # [START bigquery_label_table]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you want to create.
    table_id = "your-project.your_dataset.your_table_name"

    # [END bigquery_label_table]
    table_id = orig_table_id
    # [START bigquery_label_table]
    table = client.get_table(table_id)  # API request

    labels = {"color": "green"}
    table.labels = labels

    table = client.update_table(table, ["labels"])  # API request

    print(f"Added {table.labels} to {table_id}.")
    # [END bigquery_label_table]
