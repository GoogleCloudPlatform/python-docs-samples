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


def client_load_partitioned_table(table_id: str) -> None:

    # [START bigquery_load_table_partitioned]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("post_abbr", "STRING"),
            bigquery.SchemaField("date", "DATE"),
        ],
        skip_leading_rows=1,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="date",  # Name of the column to use for partitioning.
            expiration_ms=7776000000,  # 90 days.
        ),
    )
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states-by-date.csv"

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Wait for the job to complete.

    table = client.get_table(table_id)
    print("Loaded {} rows to table {}".format(table.num_rows, table_id))
    # [END bigquery_load_table_partitioned]
