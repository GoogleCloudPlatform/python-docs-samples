# Copyright 2022 Google LLC
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

import datetime
import time

from airflow.models import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'start_date': datetime.datetime(2022, 4, 1),
}

with DAG('parallel_work',
         default_args=default_args,
         schedule_interval=None) as dag:

    def do_work() -> None:
        import logging
        logging.info('Doing work')
        time.sleep(60)
        logging.info('Done!')

    # 12 pipelines with 6 consecutive tasks each.
    for i in range(12):
        tasks = []
        for j in range(6):
            task = PythonOperator(
                task_id=f'work-{i}-{j}',
                python_callable=do_work)
            if tasks:
                tasks[-1] >> task
            tasks.append(task)
