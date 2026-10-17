# Copyright 2024 Google LLC
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


def restore_multiple_tables(
    project_id: str, dataset_id: str, dest_dataset_id: str, region: str
) -> None:
    # [START bigquery_restore_multiple_tables]
    from concurrent.futures import ThreadPoolExecutor
    from google.cloud import bigquery

    # TODO(developer): Update these variables with your project information.
    # project_id = "your-project"
    # dataset_id = "your_source_dataset"
    # dest_dataset_id = "your_destination_dataset"
    # region = "region-us"

    client = bigquery.Client(project=project_id)

    def get_deleted_tables():
        """Queries INFORMATION_SCHEMA to find deleted tables and calculate time travel timestamps."""
        query = f"""
        SELECT
            table_name,
            # Subtract 1 millisecond from the deletion time to ensure the time travel
            # timestamp resolves to the table state just before it was deleted.
            UNIX_MILLIS(table_deletion_time) - 1 AS snapshot_millis
        FROM
            `{project_id}`.`{region}`.INFORMATION_SCHEMA.TABLE_STORAGE
        WHERE
            table_schema = @dataset_id
            AND deleted = True
        """
        print("Querying INFORMATION_SCHEMA for deleted tables...")
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("dataset_id", "STRING", dataset_id)
            ]
        )
        query_job = client.query(query, job_config=job_config)
        return list(query_job.result())

    def copy_table(row):
        """Restores a deleted table using a time decorator."""
        src_table = f"{project_id}.{dataset_id}.{row.table_name}@{row.snapshot_millis}"
        dest_table = f"{project_id}.{dest_dataset_id}.{row.table_name}"

        try:
            job = client.copy_table(src_table, dest_table)
            job.result()  # Wait for the job to complete
            print(f"Successfully restored {row.table_name} to {dest_table}")
        except Exception as ex:
            print(f"Failed to restore {row.table_name}: {ex}")

    deleted_tables = get_deleted_tables()
    if not deleted_tables:
        print("No deleted tables found in the specified dataset.")
        return

    print(f"Found {len(deleted_tables)} deleted tables. Starting restoration...")
    # Use ThreadPoolExecutor to run copy jobs concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        for row in deleted_tables:
            executor.submit(copy_table, row)

    # [END bigquery_restore_multiple_tables]
