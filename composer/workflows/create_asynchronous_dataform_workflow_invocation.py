# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START composer_dataform_async_workflow_invocation]
"""
Example Airflow DAG that creates a Dataform compilation result, starts an asynchronous Dataform workflow invocation, and
polls the status of the workflow until it enters a desired state by using DataformWorkflowInvocationStateSensor.
This Airflow DAG uses Google Dataform Airflow operators. For more information about Google Dataform Airflow operators,
see https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/dataform.html?highlight=dataform#google-dataform-operators
"""

import datetime

from airflow import models
from airflow.providers.google.cloud.operators.dataform import (
    DataformCreateCompilationResultOperator,
    DataformCreateWorkflowInvocationOperator,
)
from airflow.providers.google.cloud.sensors.dataform import (
    DataformWorkflowInvocationStateSensor,
)
from google.cloud.dataform_v1beta1 import WorkflowInvocation


DAG_ID = "dataform"
PROJECT_ID = "my_project_ID"  # Replace with your Dataform Google Cloud Project ID
REPOSITORY_ID = "my_repository_ID"  # Replace with the name of your Dataform repository
REGION = (
    "us-central1"  # Replace with the region in which the Dataform repository is located
)
GIT_COMMITISH = (
    "main"  # Replace with the Git branch or a Git SHA in your remote Git repository
)

with models.DAG(
    DAG_ID,
    schedule_interval="@once",  # Override to match your needs
    start_date=datetime.datetime(2022, 1, 1),
    catchup=False,  # Override to match your needs
    tags=["dataform"],
) as dag:

    create_compilation_result = DataformCreateCompilationResultOperator(
        task_id="create_compilation_result",
        project_id=PROJECT_ID,
        region=REGION,
        repository_id=REPOSITORY_ID,
        compilation_result={
            "git_commitish": GIT_COMMITISH,
        },
    )

create_workflow_invocation = DataformCreateWorkflowInvocationOperator(
    task_id="create_workflow_invocation",
    project_id=PROJECT_ID,
    region=REGION,
    repository_id=REPOSITORY_ID,
    asynchronous=True,
    workflow_invocation={
        "compilation_result": "{{ task_instance.xcom_pull('create_compilation_result')['name'] }}"
    },
)

is_workflow_invocation_done = DataformWorkflowInvocationStateSensor(
    task_id="is_workflow_invocation_done",
    project_id=PROJECT_ID,
    region=REGION,
    repository_id=REPOSITORY_ID,
    # workflow_invocation_id is last element of full resource name generated in create_workflow_invocation
    workflow_invocation_id=(
        "{{ task_instance.xcom_pull('create_workflow_invocation')['name'].split('/')[-1] }}"
    ),
    expected_statuses={WorkflowInvocation.State.SUCCEEDED},
)

# NOTE: is_workflow_invocation_done waits for workflow completion, it might take significant amount of time to finish depending on the project
create_compilation_result >> create_workflow_invocation >> is_workflow_invocation_done
# [END composer_dataform_async_workflow_invocation]
