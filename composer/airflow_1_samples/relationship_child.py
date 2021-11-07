# Copyright 2021 Google LLC
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
# [START composer_relationship_child_airflow_1]
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago


DAG_NAME = 'dag-to-trigger'

args = {'owner': 'airflow', 'start_date': days_ago(1), 'schedule_interval': "None"}

with DAG(dag_id=DAG_NAME, default_args=args) as dag:
    dag_task = DummyOperator(
        task_id='dag-task'
    )
# [END composer_relationship_child_airflow_1]
