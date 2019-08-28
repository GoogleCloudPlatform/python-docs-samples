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


def browse_table_data(client, table_id):

    # [START bigquery_browse_table]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to browse data rows.
    # table_id = "your-project.your_dataset.your_table_name"

    # Download all rows from a table.
    rows_iter = client.list_rows(table_id)

    # Iterate over rows to make the API requests to fetch row data.
    rows = list(rows_iter)
    print("Downloaded {} rows from table {}".format(len(rows), table_id))

    # Download at most 10 rows.
    rows_iter = client.list_rows(table_id, max_results=10)
    rows = list(rows_iter)
    print("Downloaded {} rows from table {}".format(len(rows), table_id))

    # Specify selected fields to limit the results to certain columns.
    table = client.get_table(table_id)
    fields = table.schema[:2]  # first two columns
    rows_iter = client.list_rows(table_id, selected_fields=fields, max_results=10)
    rows = list(rows_iter)
    print("Selected {} columns from table {}.".format(len(rows_iter.schema), table_id))
    print("Downloaded {} rows from table {}".format(len(rows), table_id))
    # [END bigquery_browse_table]
