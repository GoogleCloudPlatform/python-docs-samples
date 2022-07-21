# Copyright 2020 Google LLC
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

# [START composer_dataproc_workflow_instantiate_operator_tutorial_airflow_1]

"""Example Airflow DAG that kicks off a Cloud Dataproc Template that runs a
Spark Pi Job.

This DAG relies on an Airflow variable
https://airflow.apache.org/docs/apache-airflow/stable/concepts/variables.html
* project_id - Google Cloud Project ID to use for the Cloud Dataproc Template.
"""

import datetime

from airflow import models
from airflow.contrib.operators import dataproc_operator
from airflow.utils.dates import days_ago

project_id = "{{var.value.project_id}}"


default_args = {
    # Tell airflow to start one day ago, so that it runs as soon as you upload it
    "start_date": days_ago(1),
    "project_id": project_id,
}

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
    # The id you will see in the DAG airflow page
    "dataproc_workflow_dag",
    default_args=default_args,
    # The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(days=1),  # Override to match your needs
) as dag:

    start_template_job = dataproc_operator.DataprocWorkflowTemplateInstantiateOperator(
        # The task id of your job
        task_id="dataproc_workflow_dag",
        # The template id of your workflow
        template_id="sparkpi",
        project_id=project_id,
        # The region for the template
        # For more info on regions where Dataflow is available see:
        # https://cloud.google.com/dataflow/docs/resources/locations
        region="us-central1",
    )

# [END composer_dataproc_workflow_instantiate_operator_tutorial_airflow_1]
