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


def create_table(client, table_id):

    # [START bigquery_create_table]
    from google.cloud import bigquery

    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create
    # table_id = "your-project.your_dataset.your_table_name"

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # API request
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    # [END bigquery_create_table]
