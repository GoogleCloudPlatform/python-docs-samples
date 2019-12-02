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


def copy_table_multiple_source(client, dest_table_id, table_ids):

    # [START bigquery_copy_table_multiple_source]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set dest_table_id to the ID of the destination table.
    # dest_table_id = "your-project.your_dataset.your_table_name"

    # TODO(developer): Set table_ids to the list of the IDs of the original tables.
    # table_ids = ["your-project.your_dataset.your_table_name", ...]

    job = client.copy_table(table_ids, dest_table_id)  # Make an API request.
    job.result()  # Wait for the job to complete.

    print("The tables {} have been appended to {}".format(table_ids, dest_table_id))
    # [END bigquery_copy_table_multiple_source]
