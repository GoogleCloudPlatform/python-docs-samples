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

import datetime


def update_table_expiration(table_id, expiration):
    orig_table_id = table_id
    orig_expiration = expiration

    # [START bigquery_update_table_expiration]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you want to update.
    table_id = "your-project.your_dataset.your_table_name"

    # TODO(dev): Set table to expire for desired days days from now.
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=5
    )
    # [END bigquery_update_table_expiration]

    table_id = orig_table_id
    expiration = orig_expiration

    # [START bigquery_update_table_expiration]
    table = client.get_table(table_id)  # Make an API request.
    table.expires = expiration
    table = client.update_table(table, ["expires"])  # API request

    print(f"Updated {table_id}, expires {table.expires}.")
    # [END bigquery_update_table_expiration]
