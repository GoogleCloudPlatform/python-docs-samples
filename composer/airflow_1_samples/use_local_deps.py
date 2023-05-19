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

"""A DAG consisting of a BashOperator that prints the result of a coin flip."""

import datetime

import airflow
from airflow.operators import bash_operator

# [START composer_dag_local_deps_airflow_1]
from dependencies import coin_module
# [END composer_dag_local_deps_airflow_1]

default_args = {
    'start_date':
        datetime.datetime.combine(
            datetime.datetime.today() - datetime.timedelta(days=1),
            datetime.datetime.min.time()),
}

with airflow.DAG(
        'composer_sample_dependencies_dag',
        default_args=default_args) as dag:
    t1 = bash_operator.BashOperator(
        task_id='print_coin_result',
        bash_command=f'echo "{coin_module.flip_coin()}"',
        dag=dag)
