# Copyright 2018 Google LLC
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

"""Demonstrates how to use connections in an Airflow DAG."""

import datetime

from airflow import models
from airflow.providers.google.cloud.operators import bigquery


yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
}

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
        'composer_sample_connections',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    # [START composer_connections_default]
    task_default = bigquery.BigQueryInsertJobOperator(
        task_id='task_default_connection',
        configuration={
            "query": {
                "query": 'SELECT 1',
                "useLegacySql": False
            }
        }
    )
    # [END composer_connections_default]
    # [START composer_connections_explicit]
    # Composer creates a 'google_cloud_default' connection by default.
    task_explicit = bigquery.BigQueryInsertJobOperator(
        task_id='task_explicit_connection',
        gcp_conn_id='google_cloud_default',
        configuration={
            "query": {
                "query": 'SELECT 1',
                "useLegacySql": False
            }
        }
    )
    # [END composer_connections_explicit]
    # [START composer_connections_custom]
    # Set a gcp_conn_id to use a connection that you have created.
    task_custom = bigquery.BigQueryInsertJobOperator(
        task_id='task_custom_connection',
        gcp_conn_id='my_gcp_connection',
        configuration={
            "query": {
                "query": 'SELECT 1',
                "useLegacySql": False
            }
        }
    )
    # [END composer_connections_custom]
