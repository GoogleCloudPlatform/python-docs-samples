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
from unittest import mock

import pytest
import requests

import composer2_airflow_rest_api

COMPOSER2_WEB_SERVER_URL = os.environ["COMPOSER2_WEB_SERVER_URL"]
DAG_CONFIG = {"test": "value"}


@pytest.fixture(scope="function")
def successful_response():
    response_mock = mock.create_autospec(requests.Response, instance=True)
    response_mock.status_code = 200
    response_mock.text = '"state": "running"'
    with mock.patch(
        "composer2_airflow_rest_api.make_composer2_web_server_request",
        return_value=response_mock,
    ):
        yield


@pytest.fixture(scope="function")
def insufficient_permissions_response():
    response_mock = mock.Mock()
    response_mock.status_code = 403
    response_mock.text = "Mocked insufficient permissions"
    with mock.patch(
        "composer2_airflow_rest_api.make_composer2_web_server_request",
        return_value=response_mock,
    ):
        yield


def test_trigger_dag_insufficient_permissions(insufficient_permissions_response):
    with pytest.raises(requests.HTTPError) as e:
        dag_config = DAG_CONFIG
        print(
            composer2_airflow_rest_api.trigger_dag(
                COMPOSER2_WEB_SERVER_URL, "airflow_monitoring", dag_config
            )
        )
    assert "You do not have a permission to perform this operation." in str(e)


def test_trigger_dag_incorrect_environment():
    with pytest.raises(Exception) as e:
        dag_config = DAG_CONFIG
        print(
            composer2_airflow_rest_api.trigger_dag(
                "https://invalid-environment.composer.googleusercontent.com",
                "airflow_monitoring",
                dag_config,
            )
        )
    assert "Bad request" in str(e)


def test_trigger_dag(successful_response, capsys):
    dag_config = DAG_CONFIG
    print(
        composer2_airflow_rest_api.trigger_dag(
            COMPOSER2_WEB_SERVER_URL, "airflow_monitoring", dag_config
        )
    )
    out, _ = capsys.readouterr()
    assert '"state": "running"' in out
