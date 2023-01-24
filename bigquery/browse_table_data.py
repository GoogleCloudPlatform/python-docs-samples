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


def browse_table_data(table_id: str) -> None:

    # [START bigquery_browse_table]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to browse data rows.
    # table_id = "your-project.your_dataset.your_table_name"

    # Download all rows from a table.
    rows_iter = client.list_rows(table_id)  # Make an API request.

    # Iterate over rows to make the API requests to fetch row data.
    rows = list(rows_iter)
    print("Downloaded {} rows from table {}".format(len(rows), table_id))

    # Download at most 10 rows.
    rows_iter = client.list_rows(table_id, max_results=10)
    rows = list(rows_iter)
    print("Downloaded {} rows from table {}".format(len(rows), table_id))

    # Specify selected fields to limit the results to certain columns.
    table = client.get_table(table_id)  # Make an API request.
    fields = table.schema[:2]  # First two columns.
    rows_iter = client.list_rows(table_id, selected_fields=fields, max_results=10)
    print("Selected {} columns from table {}.".format(len(rows_iter.schema), table_id))

    rows = list(rows_iter)
    print("Downloaded {} rows from table {}".format(len(rows), table_id))

    # Print row data in tabular format.
    rows_iter = client.list_rows(table_id, max_results=10)
    format_string = "{!s:<16} " * len(rows_iter.schema)
    field_names = [field.name for field in rows_iter.schema]
    print(format_string.format(*field_names))  # Prints column headers.

    for row in rows_iter:
        print(format_string.format(*row))  # Prints row data.
    # [END bigquery_browse_table]
