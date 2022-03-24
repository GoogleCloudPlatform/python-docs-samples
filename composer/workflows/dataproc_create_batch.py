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
    DataprocCreateBatchOperator, DataprocDeleteBatchOperator, DataprocGetBatchOperator, DataprocListBatchesOperator

)
from airflow.utils.dates import days_ago

PROJECT_ID = "{{ var.value.project_id }}"
REGION = "{{ var.value.region_name}}"
BUCKET = "{{ var.value.bucket_name }}"
PHS_CLUSTER = "{{ var.value.phs_cluster }}"
METASTORE_CLUSTER = "{{var.value.metastore_cluster}}"
DOCKER_IMAGE = "{{var.value.image_name}}"

SPARK_ML_FILE_LOCATION = "gs://{{var.value.bucket_name }}/natality_sparkml.py"
# for e.g.  "gs//my-bucket/natality_sparkml.py"
# Start a single node Dataproc Cluster for viewing Persistent History of Spark jobs
PHS_CLUSTER_PATH = \
    "projects/{{ var.value.project_id }}/regions/{{ var.value.dataproc_region}}/clusters/{{ var.value.phs_cluster }}"
# for e.g. projects/my-project/regions/my-region/clusters/my-cluster"
SPARK_BIGQUERY_JAR_FILE = "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
# Start a Dataproc MetaStore Cluster
METASTORE_SERVICE_LOCATION = \
    "projects/{{var.value.project_id}}/locations/{{var.value.region_name}}/services/{{var.value.metastore_cluster }}"
# for e.g. projects/my-project/locations/my-region/services/my-cluster
CUSTOM_CONTAINER = "us.gcr.io/{{var.value.project_id}}/{{ var.value.image_name}}"
# for e.g. "us.gcr.io/my-project/quickstart-image",

default_args = {
    # Tell airflow to start one day ago, so that it runs as soon as you upload it
    "start_date": days_ago(1),
    "project_id": PROJECT_ID,
    "region": REGION,

}
with models.DAG(
    "dataproc_batch_operators",  # The id you will see in the DAG airflow page
    default_args=default_args,  # The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(days=1),  # Override to match your needs
) as dag:

    create_batch = DataprocCreateBatchOperator(
        task_id="batch_create",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": SPARK_ML_FILE_LOCATION,
                "jar_file_uris": [SPARK_BIGQUERY_JAR_FILE],
            },
            "environment_config": {
                "peripherals_config": {
                    "spark_history_server_config": {
                        "dataproc_cluster": PHS_CLUSTER_PATH,
                    },
                },
            },
        },
        batch_id="batch_create_phs",
    )
    # [START composer_dataproc_list_batch]
    list_batches = DataprocListBatchesOperator(
        task_id="list_all_batches",
    )
    # [END composer_dataproc_list_batch]

    # [START composer_dataproc_get_batch]
    get_batch = DataprocGetBatchOperator(
        task_id="get_batch",
        batch_id="batch_create_phs",
    )
    # [END composer_dataproc_get_batch]
    # [START composer_dataproc_delete_batch]
    delete_batch = DataprocDeleteBatchOperator(
        task_id="delete_batch",
        batch_id="batch_create_phs",
    )
    # [END composer_dataproc_delete_batch]
    create_batch >> list_batches >> get_batch >> delete_batch
    # [END composer_dataproc_create_batch]

    # [START composer_dataproc_create_metastore_batch]
    create_batch_with_metastore = DataprocCreateBatchOperator(
        task_id="dataproc_metastore",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": SPARK_ML_FILE_LOCATION,
                "jar_file_uris": [SPARK_BIGQUERY_JAR_FILE],
            },
            "environment_config": {
                "peripherals_config": {
                    "metastore_service": METASTORE_SERVICE_LOCATION,
                    "spark_history_server_config": {
                        "dataproc_cluster": PHS_CLUSTER_PATH,
                    },
                 },
            },
        },
        batch_id="dataproc_metastore",
    )
    get_batch_metastore = DataprocGetBatchOperator(
        task_id="get_batch_metatstore",
        batch_id="dataproc_metastore",
    )
    delete_batch_metastore = DataprocDeleteBatchOperator(
        task_id="delete_batch_metastore",
        batch_id="dataproc_metastore",
    )

    create_batch_with_metastore >> get_batch_metastore >> delete_batch_metastore

    # [END composer_dataproc_create_metastore_batch]

    # [START composer_dataproc_create_custom_container]
    create_batch_with_custom_container = DataprocCreateBatchOperator(
        task_id="dataproc_custom_container",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": SPARK_ML_FILE_LOCATION,
                "jar_file_uris": [SPARK_BIGQUERY_JAR_FILE],
            },
            "environment_config": {
                "peripherals_config": {
                     "spark_history_server_config": {
                        "dataproc_cluster": PHS_CLUSTER_PATH,
                     },
                 },
            },
            "runtime_config": {
                    "container_image": CUSTOM_CONTAINER,
                },
        },
        batch_id="batch_custom_container",
    )
    get_batch_custom = DataprocGetBatchOperator(
        task_id="get_batch_custom",
        batch_id="batch_custom_container",
    )
    delete_batch_custom = DataprocDeleteBatchOperator(
        task_id="delete_batch_custom",
        batch_id="batch_custom_container",
    )
    create_batch_with_custom_container >> get_batch_custom >> delete_batch_custom
    # [END composer_dataproc_create_custom_container]
