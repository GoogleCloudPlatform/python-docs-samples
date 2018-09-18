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

"""An example DAG demonstrating a cyle in the task IDs."""

import datetime

from airflow import models
from airflow.operators import dummy_operator


yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

default_dag_args = {
    'start_date': yesterday,
}

with models.DAG(
        'composer_sample_cycle',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    start = dummy_operator.DummyOperator(task_id='oops_a_cycle')
    end = dummy_operator.DummyOperator(task_id='oops_a_cycle')
    start >> end
