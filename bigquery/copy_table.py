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


def copy_table(source_table_id: str, destination_table_id: str) -> None:
    # [START bigquery_copy_table]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set source_table_id to the ID of the original table.
    # source_table_id = "your-project.source_dataset.source_table"

    # TODO(developer): Set destination_table_id to the ID of the destination table.
    # destination_table_id = "your-project.destination_dataset.destination_table"

    job = client.copy_table(source_table_id, destination_table_id)
    job.result()  # Wait for the job to complete.

    print("A copy of the table created.")
    # [END bigquery_copy_table]
