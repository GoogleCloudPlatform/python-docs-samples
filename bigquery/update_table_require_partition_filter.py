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


def update_table_require_partition_filter(table_id: str) -> None:
    # [START bigquery_update_table_require_partition_filter]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the model to fetch.
    # table_id = 'your-project.your_dataset.your_table'

    table = client.get_table(table_id)  # Make an API request.
    table.require_partition_filter = True
    table = client.update_table(table, ["require_partition_filter"])

    # View table properties
    print(
        "Updated table '{}.{}.{}' with require_partition_filter={}.".format(
            table.project,
            table.dataset_id,
            table.table_id,
            table.require_partition_filter,
        )
    )
    # [END bigquery_update_table_require_partition_filter]
