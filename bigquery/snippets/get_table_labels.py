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


def get_table_labels(table_id: str) -> None:
    orig_table_id = table_id
    # [START bigquery_get_table_labels]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you want to create.
    table_id = "your-project.your_dataset.your_table_name"

    # [END bigquery_get_table_labels]
    table_id = orig_table_id

    # [START bigquery_get_table_labels]
    table = client.get_table(table_id)  # API Request

    # View table labels
    print(f"Table ID: {table_id}.")
    if table.labels:
        for label, value in table.labels.items():
            print(f"\t{label}: {value}")
    else:
        print("\tTable has no labels defined.")
    # [END bigquery_get_table_labels]
