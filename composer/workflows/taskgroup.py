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

# [START composer_taskgroup]
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

with DAG(dag_id="taskgroup_example", start_date=days_ago(1)) as dag:
    start = DummyOperator(task_id="start")

    with TaskGroup("taskgroup_1", tooltip="task group #1") as section_1:
        task_1 = BashOperator(task_id="op-1", bash_command=':')
        task_2 = BashOperator(task_id="op-2", bash_command=':')

    with TaskGroup("taskgroup_2", tooltip="task group #2") as section_2:
        task_3 = BashOperator(task_id="op-3", bash_command=':')
        task_4 = BashOperator(task_id="op-4", bash_command=':')

    some_other_task = DummyOperator(
        task_id='some-other-task'
    )

    end = DummyOperator(task_id='end')

    start >> section_1 >> some_other_task >> section_2 >> end
# [END composer_taskgroup]
