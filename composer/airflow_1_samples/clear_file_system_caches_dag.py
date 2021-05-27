# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A dag that prevents memory leaks on scheduler and workers."""
from datetime import timedelta
import os

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG(
    'clear_file_system_caches_dag',
    description='clear file system caches on scheduler and workers',
    schedule_interval='*/30 * * * *',
    dagrun_timeout=timedelta(minutes=20),
    start_date=airflow.utils.dates.days_ago(1),
    catchup=False)

# clean file system cache on scheduler
os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches')

# clean file system cache on one of workers
t1 = BashOperator(
    task_id='clear_caches',
    bash_command='echo 3 | sudo tee /proc/sys/vm/drop_caches',
    dag=dag,
    depends_on_past=False)

t1
