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

from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator


DATASET = 'airflow-summit-2022-data.holiday_weather'
TABLE = 'holidays'

default_args = {
    'start_date': datetime(2022, 4, 1),
    'retry_delay': timedelta(seconds=1)
}

with DAG('bigquery_permissions',
         default_args=default_args,
         schedule_interval=None) as dag:

    check_count = BigQueryCheckOperator(
        task_id="check_count",
        sql=f'SELECT COUNT(*) FROM {DATASET}.{TABLE}',
        use_legacy_sql=False,
    )
