# Copyright 2023 Google LLC
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

# [START composer_check_moved_tables]
"""
When upgrading Airflow to a newer version,
it might happen that some data cannot be migrated,
often because of constraint changes in the metadata base.
This file contains 2 DAGs:

1. 'list_moved_tables_after_upgrade_dag'
  Prints the rows which failed to be migrated.
2. 'rename_moved_tables_after_upgrade_dag'
  Renames the table which contains the failed migrations. This will remove the
  warning message from airflow.
"""

import datetime
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.settings import AIRFLOW_MOVED_TABLE_PREFIX


def get_moved_tables():
    hook = PostgresHook(postgres_conn_id="airflow_db")
    return hook.get_records(
        "SELECT schemaname, tablename FROM pg_catalog.pg_tables WHERE tablename"
        f" LIKE '{AIRFLOW_MOVED_TABLE_PREFIX}_%'"
    )


def list_moved_records():
    tables = get_moved_tables()
    if not tables:
        logging.info("No moved tables found")
        return

    hook = PostgresHook(postgres_conn_id="airflow_db")
    for schema, table in tables:
        df = hook.get_pandas_df(f"SELECT * FROM {schema}.{table}")
        logging.info(df.to_markdown())


def rename_moved_tables():
    tables = get_moved_tables()
    if not tables:
        return

    hook = PostgresHook(postgres_conn_id="airflow_db")
    for schema, table in tables:
        hook.run(f"ALTER TABLE {schema}.{table} RENAME TO _abandoned_{table}")


with DAG(
    dag_id="list_moved_tables_after_upgrade_dag",
    start_date=datetime.datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
):
    t1 = PythonOperator(
        task_id="list_moved_records", python_callable=list_moved_records
    )

with DAG(
    dag_id="rename_moved_tables_after_upgrade_dag",
    start_date=datetime.datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    t1 = PythonOperator(
        task_id="rename_moved_tables", python_callable=rename_moved_tables
    )

# [END composer_check_moved_tables]
