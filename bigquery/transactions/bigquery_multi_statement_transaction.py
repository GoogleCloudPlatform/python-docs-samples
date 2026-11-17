# Copyright 2026 Google LLC
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

# [START bigquery_multi_statement_transaction]
from google.cloud import bigquery


def run_multi_statement_transaction(
    project_id: str,
    dataset_id: str,
    source_table_id: str,
    target_table_id: str,
) -> None:
    """Executes a multi-statement SQL transaction with exception rollback handling.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the tables
            (for example, 'example_dataset').
        source_table_id: Source staging table ID to merge and clear
            (for example, 'example_new_arrivals').
        target_table_id: Target inventory table ID to update atomically
            (for example, 'example_inventory').
    """
    client = bigquery.Client(project=project_id)
    source_ref = f"{project_id}.{dataset_id}.{source_table_id}"
    target_ref = f"{project_id}.{dataset_id}.{target_table_id}"
    # BigQuery scopes a multi-statement transaction to a single script query job, spawning child
    # jobs for each statement and rolling back uncommitted changes on error.
    transaction_sql = f"""
        BEGIN
          BEGIN TRANSACTION;
          MERGE `{target_ref}` AS inv
          USING `{source_ref}` AS src
          ON inv.product = src.product
          WHEN MATCHED THEN
            UPDATE SET quantity = inv.quantity + src.quantity
          WHEN NOT MATCHED THEN
            INSERT (product, quantity) VALUES (src.product, src.quantity);
          DELETE FROM `{source_ref}` WHERE TRUE;
          COMMIT TRANSACTION;
        EXCEPTION WHEN ERROR THEN
          ROLLBACK TRANSACTION;
          RAISE USING MESSAGE = @@error.message;
        END;
    """
    select_sql = f"""
        SELECT
          COUNT(*) AS inventory_rows
        FROM `{target_ref}`;
    """

    print(f"Running multi-statement transaction into: {target_ref}")
    transaction_job = client.query(transaction_sql)
    transaction_job.result()

    count_job = client.query(select_sql)
    rows = list(count_job.result())

    inventory_rows = rows[0].inventory_rows if rows else 0
    print(f"Resource ID: {target_ref}")
    print(f"Child Jobs: {transaction_job.num_child_jobs}")
    print(f"Inventory Rows: {inventory_rows}")
    print(f"Job ID: {transaction_job.job_id}")
    print(f"Source Table: {source_ref}")
    print("Transaction State: COMMITTED")


# [END bigquery_multi_statement_transaction]
