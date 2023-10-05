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


def create_partitioned_table(table_id):
    your_fully_qualified_table_id = table_id

    # [START bigquery_create_table_partitioned]
    from google.cloud import bigquery

    client = bigquery.Client()

    # Use format "your-project.your_dataset.your_table_name" for table_id
    table_id = your_fully_qualified_table_id
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
        bigquery.SchemaField("date", "DATE"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date",  # name of column to use for partitioning
        expiration_ms=1000 * 60 * 60 * 24 * 90,
    )  # 90 days

    table = client.create_table(table)

    print(
        f"Created table {table.project}.{table.dataset_id}.{table.table_id}, "
        f"partitioned on column {table.time_partitioning.field}."
    )
    # [END bigquery_create_table_partitioned]
    return table
