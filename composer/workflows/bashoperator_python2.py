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

# [START composer_bashoperator_python2]
import datetime

from airflow import models
from airflow.operators import bash_operator


yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())


default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
}

with models.DAG(
        'composer_sample_bashoperator_python2',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    run_python2 = bash_operator.BashOperator(
        task_id='run_python2',
        # This example runs a Python script from the data folder to prevent
        # Airflow from attempting to parse the script as a DAG.
        bash_command='python2 /home/airflow/gcs/data/python2_script.py',
    )
# [END composer_bashoperator_python2]
