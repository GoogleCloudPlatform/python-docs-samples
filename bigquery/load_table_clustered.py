# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def load_table_clustered(table_id: str) -> "bigquery.Table":
    # [START bigquery_load_table_clustered]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        schema=[
            bigquery.SchemaField("timestamp", bigquery.SqlTypeNames.TIMESTAMP),
            bigquery.SchemaField("origin", bigquery.SqlTypeNames.STRING),
            bigquery.SchemaField("destination", bigquery.SqlTypeNames.STRING),
            bigquery.SchemaField("amount", bigquery.SqlTypeNames.NUMERIC),
        ],
        time_partitioning=bigquery.TimePartitioning(field="timestamp"),
        clustering_fields=["origin", "destination"],
    )

    job = client.load_table_from_uri(
        ["gs://cloud-samples-data/bigquery/sample-transactions/transactions.csv"],
        table_id,
        job_config=job_config,
    )

    job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )
    # [END bigquery_load_table_clustered]
    return table
