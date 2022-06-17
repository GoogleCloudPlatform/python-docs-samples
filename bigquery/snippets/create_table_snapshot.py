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


def create_table_snapshot(source_table_id: str, snapshot_table_id: str) -> None:
    original_source_table_id = source_table_id
    original_snapshot_table_id = snapshot_table_id
    # [START bigquery_create_table_snapshot]
    from google.cloud import bigquery

    # TODO(developer): Set table_id to the ID of the table to create.
    source_table_id = "your-project.your_dataset.your_table_name"
    snapshot_table_id = "your-project.your_dataset.snapshot_table_name"
    # [END bigquery_create_table_snapshot]
    source_table_id = original_source_table_id
    snapshot_table_id = original_snapshot_table_id
    # [START bigquery_create_table_snapshot]

    # Construct a BigQuery client object.
    client = bigquery.Client()
    copy_config = bigquery.CopyJobConfig()
    copy_config.operation_type = bigquery.OperationType.SNAPSHOT

    copy_job = client.copy_table(
        sources=source_table_id,
        destination=snapshot_table_id,
        job_config=copy_config,
    )
    copy_job.result()

    print("Created table snapshot {}".format(snapshot_table_id))
    # [END bigquery_create_table_snapshot]
