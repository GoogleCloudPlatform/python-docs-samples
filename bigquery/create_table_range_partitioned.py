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

import typing

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def create_table_range_partitioned(table_id: str) -> "bigquery.Table":
    # [START bigquery_create_table_range_partitioned]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    schema = [
        bigquery.SchemaField("full_name", "STRING"),
        bigquery.SchemaField("city", "STRING"),
        bigquery.SchemaField("zipcode", "INTEGER"),
    ]

    table = bigquery.Table(table_id, schema=schema)
    table.range_partitioning = bigquery.RangePartitioning(
        # To use integer range partitioning, select a top-level REQUIRED /
        # NULLABLE column with INTEGER / INT64 data type.
        field="zipcode",
        range_=bigquery.PartitionRange(start=0, end=100000, interval=10),
    )
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    # [END bigquery_create_table_range_partitioned]
    return table
