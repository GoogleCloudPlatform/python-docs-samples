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

"""An example DAG demonstrating use of variables and how to test it."""

import datetime

from airflow import models
from airflow.operators import bash
from airflow.operators import dummy

# If you are running Airflow in more than one time zone
# see https://airflow.apache.org/docs/apache-airflow/stable/timezone.html
# for best practices
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

default_dag_args = {
    "start_date": yesterday,
}

with models.DAG(
    "composer_sample_variables",
    schedule_interval=datetime.timedelta(days=1),
    default_args=default_dag_args,
) as dag:
    start = dummy.DummyOperator(task_id="start")
    end = dummy.DummyOperator(task_id="end")
    variable_example = bash.BashOperator(
        task_id="variable_example",
        bash_command="echo project_id=" + "{{var.value.gcp_project}}",
    )
    start >> variable_example >> end
