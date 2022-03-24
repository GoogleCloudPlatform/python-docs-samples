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

#TODOS
# [x] - orchestrate dataproc cluster creation
# [x] - orchestrate data ingestion dataproc job
# [ ] - orhcestrate data ingestion bq part
# [ ] - orchestrate data processing
# [ ] - orchestrate feature eng
# [ ] - orchestrate vertex model training
# [x] - orchestrate model deployment


import datetime
import os

from airflow import models
from airflow.providers.google.cloud.operators import dataproc
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

from airflow.utils import trigger_rule

CLUSTER_CONFIG = {
    "config_bucket": '{{var.value.gcs_bucket}}',
    "gce_cluster_config": {
        "service_account": '{{var.value.service_account}}'
    },

    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-4"
    },
    "worker_config": {
        "num_instances": 8,
        "machine_type_uri": "n1-standard-4"
    },
}

PROJECT_NAME = '{{var.value.gcp_project}}'
BQ_DATASET_NAME="new_york_citibike_trips"
# CLUSTER_NAME='data-science-onramp-cluster-{{ ds_nodash }}'
CLUSTER_NAME='data-science-onramp-cluster-20220322'
PYSPARK_JAR = 'gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar'
INGESTION_PYTHON_FILE = 'gs://{{var.value.gcs_bucket}}/ingestion.py'
INGESTION_PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_NAME},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {"main_python_file_uri": INGESTION_PYTHON_FILE, "jar_file_uris": [PYSPARK_JAR], "args": [PROJECT_NAME, BQ_DATASET_NAME]},
    
}



yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': PROJECT_NAME,
    'region': '{{ var.value.gce_region }}',

}

with models.DAG(
        'data_analytics_ml_pipeline',
        # Continue to run DAG once per day
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    # [END composer_hadoop_schedule]

    # # Create a Cloud Dataproc cluster.
    # create_dataproc_cluster = dataproc.DataprocCreateClusterOperator(
    #     task_id='create_dataproc_cluster',
    #     # Give the cluster a unique name by appending the date scheduled.
    #     # See https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html
    #     cluster_name=CLUSTER_NAME,
    #     cluster_config=CLUSTER_CONFIG,
    #     region='{{ var.value.gce_region }}'
    # )

    # # Run the ingestion job
    # run_data_ingestion = dataproc.DataprocSubmitJobOperator(
    #     task_id='run_data_ingestion',
    #     job=INGESTION_PYSPARK_JOB)


    load_external_dataset = GCSToBigQueryOperator(
        task_id='run_bq_external_ingestion',
        bucket='{{var.value.gcs_bucket}}',
        source_objects=['holidays.csv'],
        destination_project_dataset_table=f"{BQ_DATASET_NAME}.usholidays",
        source_format="CSV",
        schema_fields=[
            {"name": "Date", "type": "DATE"}, {"name": "Holiday", "type": "STRING"}
        ],
        skip_leading_rows=1,
    )
    # # Delete Cloud Dataproc cluster.
    # delete_dataproc_cluster = dataproc.DataprocDeleteClusterOperator(
    #     task_id='delete_dataproc_cluster',
    #     cluster_name=CLUSTER_NAME,
    #     region='{{ var.value.gce_region }}',
    #     # Setting trigger_rule to ALL_DONE causes the cluster to be deleted
    #     # even if the Dataproc job fails.
    #     trigger_rule=trigger_rule.TriggerRule.ALL_DONE)

    # [START composer_hadoop_steps]
    # Define DAG dependencies.
    # create_dataproc_cluster >> run_data_ingestion >> delete_dataproc_cluster
 
    load_external_dataset