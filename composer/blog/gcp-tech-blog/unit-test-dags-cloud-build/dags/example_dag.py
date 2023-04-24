# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from airflow import models

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.gcs import GCSDeleteBucketOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator

from airflow.utils.dates import days_ago
from airflow.utils.state import State

# Assumes existence of Airflow Variable set to name of GCP Project
PROJECT_ID = "{{var.value.gcp_project}}"


with models.DAG(
    "example_gcs",
    start_date=days_ago(1),
    schedule_interval=None,
) as dag:
    generate_uuid = PythonOperator(
        task_id="generate_uuid", python_callable=lambda: str(uuid.uuid4())
    )
    create_bucket = GCSCreateBucketOperator(
        task_id="create_bucket",
        bucket_name="{{ task_instance.xcom_pull('generate_uuid') }}",
        project_id=PROJECT_ID,
    )
    list_objects = GCSListObjectsOperator(
        task_id="list_objects", bucket="{{ task_instance.xcom_pull('generate_uuid') }}"
    )
    list_buckets_result = BashOperator(
        task_id="list_buckets_result",
        bash_command="echo \"{{ task_instance.xcom_pull('list_objects') }}\"",
    )
    delete_bucket = GCSDeleteBucketOperator(
        task_id="delete_bucket",
        bucket_name="{{ task_instance.xcom_pull('generate_uuid') }}",
    )

    (
        generate_uuid
        >> create_bucket
        >> list_objects
        >> list_buckets_result
        >> delete_bucket
    )


if __name__ == "__main__":
    dag.clear(dag_run_state=State.NONE)
    dag.run()
