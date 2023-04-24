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

# This DAG script is an expansion of data_analytics_dag.py that runs a more complex Dataproc job found in data_analytics_process_expansion.py

import datetime

from airflow import models
from airflow.providers.google.cloud.operators import dataproc
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow.utils.task_group import TaskGroup

PROJECT_NAME = "{{var.value.gcp_project}}"

# BigQuery configs
BQ_DESTINATION_DATASET_NAME = "precipitation_changes"
BQ_DESTINATION_TABLE_NAME = "ghcnd_stations_joined"
BQ_NORMALIZED_TABLE_NAME = "ghcnd_stations_normalized"
BQ_PRCP_MEAN_TABLE_NAME = "ghcnd_stations_prcp_mean"
BQ_SNOW_MEAN_TABLE_NAME = "ghcnd_stations_prcp_mean"
BQ_PHX_PRCP_TABLE_NAME = "phx_annual_prcp"
BQ_PHX_SNOW_TABLE_NAME = "phx_annual_snow"

# Dataproc configs
BUCKET_NAME = "{{var.value.gcs_bucket}}"
PROCESSING_PYTHON_FILE = f"gs://{BUCKET_NAME}/data_analytics_process_expansion.py"

BATCH_ID = "data-processing-{{ ts_nodash | lower}}"  # Dataproc serverless only allows lowercase characters
BATCH_CONFIG = {
    "runtime_config": {
        "version": "1.1"
    },
    "pyspark_batch": {
        "main_python_file_uri": PROCESSING_PYTHON_FILE,
        "args": [
            BUCKET_NAME,
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_DESTINATION_TABLE_NAME}",
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_NORMALIZED_TABLE_NAME}",
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PRCP_MEAN_TABLE_NAME}",
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_SNOW_MEAN_TABLE_NAME}",
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_PRCP_TABLE_NAME}",
            f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_SNOW_TABLE_NAME}",
        ],
    },
    "environment_config": {
        "execution_config": {
            "service_account": "{{var.value.dataproc_service_account}}"
        }
    },
}

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1), datetime.datetime.min.time()
)

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    "start_date": yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    "email_on_failure": False,
    "email_on_retry": False,
}

with models.DAG(
    "data_analytics_dag_expansion",
    # Continue to run DAG once per day
    schedule_interval=datetime.timedelta(days=1),
    default_args=default_dag_args,
) as dag:
    create_batch = dataproc.DataprocCreateBatchOperator(
        task_id="create_batch",
        project_id=PROJECT_NAME,
        region="{{ var.value.gce_region }}",
        batch=BATCH_CONFIG,
        batch_id=BATCH_ID,
    )

    load_external_dataset = GCSToBigQueryOperator(
        task_id="run_bq_external_ingestion",
        bucket=BUCKET_NAME,
        source_objects=["ghcn-stations-processed.csv"],
        destination_project_dataset_table=f"{BQ_DESTINATION_DATASET_NAME}.ghcnd-stations-new",
        source_format="CSV",
        schema_fields=[
            {"name": "ID", "type": "STRING", "mode": "REQUIRED"},
            {"name": "LATITUDE", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "LONGITUDE", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "ELEVATION", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "STATE", "type": "STRING", "mode": "NULLABLE"},
            {"name": "NAME", "type": "STRING", "mode": "REQUIRED"},
        ],
        write_disposition="WRITE_TRUNCATE",
    )

    with TaskGroup("join_bq_datasets") as bq_join_group:
        for year in range(1997, 2022):
            # BigQuery configs
            BQ_DATASET_NAME = f"bigquery-public-data.ghcn_d.ghcnd_{str(year)}"
            GHCND_STATIONS_JOIN_QUERY = f"""
            SELECT Stations.ID, Stations.LATITUDE, Stations.LONGITUDE,
            Stations.STATE, Table.DATE, Table.ELEMENT, Table.VALUE
            FROM `{PROJECT_NAME}.{BQ_DESTINATION_DATASET_NAME}.ghcnd-stations-new` AS Stations, {BQ_DATASET_NAME} AS Table
            WHERE Stations.ID = Table.id
            """

            bq_join_stations_data = BigQueryInsertJobOperator(
                task_id=f"bq_join_stations_data_{str(year)}",
                configuration={
                    "query": {
                        "query": GHCND_STATIONS_JOIN_QUERY,
                        "useLegacySql": False,
                        "destinationTable": {
                            "projectId": PROJECT_NAME,
                            "datasetId": BQ_DESTINATION_DATASET_NAME,
                            "tableId": BQ_DESTINATION_TABLE_NAME,
                        },
                        "writeDisposition": "WRITE_APPEND",
                    }
                },
                location="US",
            )

        load_external_dataset >> bq_join_group >> create_batch
