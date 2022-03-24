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

# [START composer_dataproc_create_batch]

"""Example Airflow DAG that kicks off a batches job which will run a linear regression Spark ML job
This DAG relies on an Airflow variable
https://airflow.apache.org/docs/apache-airflow/stable/concepts/variables.html
* project_id - Google Cloud Project ID to use for the Cloud Dataproc Serverless.
* sparkml_file_location - Google Cloud Storage bucket where you've stored the natality_spark_ml file
* phs_cluster - Google Dataproc Cluster, a single node cluster that you have started and is running
TODO: Add the tutorial link once it is published.
"""

import datetime

from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator,
)
from airflow.utils.dates import days_ago

project_id = "{{ var.value.project_id }}"
sparkml_file_location = "gs//bucket_name/natality_sparkml.py"  # for e.g.  "gs//my-bucket/natality_sparkml.py"
# TODO: Add the location where your Spark ML python file is stored.
# Start a single node Dataproc Cluster for viewing Persistent History of Spark jobs
phs_cluster = "projects/project-ID/regions/region-name/clusters/cluster-name"
# for e.g. projects/my-project/regions/my-region/clusters/my-cluster"
spark_bigquery_jar_file = "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
metastore_service_location = "projects/project-id/locations/region-name/services/cluster-name"
# for e.g. projects/my-project/locations/my-region/services/my-cluster
custom_container = "us.gcr.io/PROJECT-ID/image-name"
# for e.g. "us.gcr.io/my-project/quickstart-image",

default_args = {
    # Tell airflow to start one day ago, so that it runs as soon as you upload it
    "start_date": days_ago(1),
    "project_id": project_id,
}

with models.DAG(
    "dataproc_create_batch_operator",  # The id you will see in the DAG airflow page
    default_args=default_args,  # The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(days=1),  # Override to match your needs
) as dag:

    create_batch = DataprocCreateBatchOperator(
        task_id="batch-create",
        project_id=project_id,
        region="us-central1",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": sparkml_file_location,
                "jar_file_uris": [spark_bigquery_jar_file],
            },
            "environment_config": {
                "peripherals_config": {
                    "spark_history_server_config": {
                        "dataproc_cluster": phs_cluster,
                    },
                },
            },
        },
        batch_id="batch-create-phs",
    )

    # [END composer_dataproc_create_batch]

    # [START composer_dataproc_create_metastore_batch]

    create_batch_with_metastore = DataprocCreateBatchOperator(
        task_id="dataproc-metastore",
        project_id=project_id,
        region="us-central1",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": sparkml_file_location,
                "jar_file_uris": [spark_bigquery_jar_file],
            },
            "environment_config": {
                "peripherals_config": {
                    "metastore_service": metastore_service_location,
                    "spark_history_server_config": {
                        "dataproc_cluster": phs_cluster,
                    },
                 },
            },
        },
        batch_id="dataproc-metastore",
    )

    # [END composer_dataproc_create_metastore_batch]
    # [START composer_dataproc_create_custom_container]
    create_batch_with_custom_container = DataprocCreateBatchOperator(
        task_id="dataproc-custom-container",
        project_id=project_id,
        region="us-central1",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": sparkml_file_location,
                "jar_file_uris": [spark_bigquery_jar_file],
            },
            "environment_config": {
                "peripherals_config": {
                     "spark_history_server_config": {
                        "dataproc_cluster": phs_cluster,
                     },
                 },
            },
            "runtime_config": {
                    "container_image": custom_container,
                },
        },
        batch_id="batch-custom-container",
    )
    # [END composer_dataproc_create_custom_container_batch]
