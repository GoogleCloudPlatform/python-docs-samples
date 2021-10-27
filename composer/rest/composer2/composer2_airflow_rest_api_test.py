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

import os

from composer2_airflow_rest_api import trigger_dag

COMPOSER2_WEB_SERVER_URL = os.environ['COMPOSER2_WEB_SERVER_URL']

def test_trigger_dag(capsys):
    dag_config = { "test": "value" }
    # Trigger the airflow_monitoring DAG, which is available in all environments by default
    print(trigger_dag(COMPOSER2_WEB_SERVER_URL, 'airflow_monitoring', dag_config))
    out, _ = capsys.readouterr()
    assert '"state": "running"' in out
