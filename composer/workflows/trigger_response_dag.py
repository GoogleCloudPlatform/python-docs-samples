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

"""DAG running in response to a Cloud Storage bucket change."""

# [START composer_trigger_response_dag]
import datetime

import airflow
from airflow.operators.bash import BashOperator


with airflow.DAG(
    "composer_sample_trigger_response_dag",
    start_date=datetime.datetime(2021, 1, 1),
    # Not scheduled, trigger only
    schedule_interval=None,
) as dag:
    # Print the dag_run's configuration, which includes information about the
    # Cloud Storage object change.
    print_gcs_info = BashOperator(
        task_id="print_gcs_info", bash_command="echo {{ dag_run.conf }}"
    )
# [END composer_trigger_response_dag]
