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

import composer2_airflow_rest_api  # noqa: I100

COMPOSER2_WEB_SERVER_URL = os.environ["COMPOSER2_WEB_SERVER_URL"]
DAG_CONFIG = {"test": "value"}


@pytest.fixture(scope="function")
def successful_response() -> None:
    response_mock = mock.create_autospec(requests.Response, instance=True)
    response_mock.status_code = 200
    response_mock.text = '"state": "running"'
    response_mock.headers = {"Content-Type": "text/html; charset=utf-8"}

    with mock.patch(
        "composer2_airflow_rest_api.make_composer2_web_server_request",
        autospec=True,
        return_value=response_mock,
    ):
        yield


@pytest.fixture(scope="function")
def insufficient_permissions_response() -> None:
    response_mock = mock.create_autospec(requests.Response, instance=True)
    response_mock.status_code = 403
    response_mock.text = "Mocked insufficient permissions"
    response_mock.headers = {"Content-Type": "text/html; charset=utf-8"}
    with mock.patch(
        "composer2_airflow_rest_api.make_composer2_web_server_request",
        autospec=True,
        return_value=response_mock,
    ):
        yield


def test_trigger_dag_insufficient_permissions(insufficient_permissions_response: None) -> None:
    with pytest.raises(
        requests.HTTPError,
        match="You do not have a permission to perform this operation.",
    ):
        composer2_airflow_rest_api.trigger_dag(
            COMPOSER2_WEB_SERVER_URL, "airflow_monitoring", DAG_CONFIG
        )


def test_trigger_dag_incorrect_environment() -> None:
    with pytest.raises(requests.HTTPError, match="404 Client Error: Not Found for url"):
        composer2_airflow_rest_api.trigger_dag(
            "https://invalid-environment.composer.googleusercontent.com",
            "airflow_monitoring",
            DAG_CONFIG,
        )


def test_trigger_dag(successful_response: None) -> None:
    out = composer2_airflow_rest_api.trigger_dag(
        COMPOSER2_WEB_SERVER_URL, "airflow_monitoring", DAG_CONFIG
    )
    assert '"state": "running"' in out
