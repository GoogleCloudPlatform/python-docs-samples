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

# [START composer_dataproc_dag]

"""Example Airflow DAG that get a specific Serverless Dataproc Batch that exists in a project
This DAG relies on an Airflow variable
https://airflow.apache.org/docs/apache-airflow/stable/concepts/variables.html
* project_id - Google Cloud Project ID to use for the Cloud Dataproc Serverless.
"""

import datetime
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import DataprocGetBatchOperator
from airflow.utils.dates import days_ago

project_id = '{{ var.value.project_id }}'

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

    get_batch = DataprocGetBatchOperator(
        task_id="get_batch",
        project_id=project_id,
        region="us-central1",
        batch_id="my-batch"
    )

    list_batches > get_batch
