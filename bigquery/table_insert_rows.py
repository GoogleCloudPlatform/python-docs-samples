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


def table_insert_rows(client, table_id):

    # [START bigquery_table_insert_rows]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the model to fetch.
    # table_id = "your-project.your_dataset.your_table"

    table = client.get_table(table_id)  # Make an API request.
    rows_to_insert = [(u"Phred Phlyntstone", 32), (u"Wylma Phlyntstone", 29)]

    errors = client.insert_rows(table, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    # [END bigquery_table_insert_rows]
