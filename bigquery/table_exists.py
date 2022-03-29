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


def table_exists(table_id: str) -> None:

    # [START bigquery_table_exists]
    from google.cloud import bigquery
    from google.cloud.exceptions import NotFound

    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to determine existence.
    # table_id = "your-project.your_dataset.your_table"

    try:
        client.get_table(table_id)  # Make an API request.
        print("Table {} already exists.".format(table_id))
    except NotFound:
        print("Table {} is not found.".format(table_id))
    # [END bigquery_table_exists]
