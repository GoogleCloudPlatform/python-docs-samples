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
# [START composer_relationship_parent_airflow_1]
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago


with DAG(
    dag_id="controller_dag_to_trigger_other_dags",
    default_args={"owner": "airflow"},
    start_date=days_ago(1),
    schedule_interval="@once",
) as dag:
    start = DummyOperator(
        task_id='start'
    )

    trigger_1 = TriggerDagRunOperator(
        task_id="dag_1",
        trigger_dag_id="dag-to-trigger",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"message": "Hello World"}
    )
    trigger_2 = TriggerDagRunOperator(
        task_id="dag_2",
        trigger_dag_id="dag-to-trigger",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"message": "Hello World"}
    )

    some_other_task = DummyOperator(
        task_id='some-other-task'
    )

    end = DummyOperator(
        task_id='end'
    )

    start >> trigger_1 >> some_other_task >> trigger_2 >> end
# [END composer_relationship_parent_airflow_1]
