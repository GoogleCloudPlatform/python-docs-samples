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

from google.cloud.bigquery_connection_v1.services import connection_service
import pytest


@pytest.fixture(scope="session")
def connection_client() -> connection_service.ConnectionServiceClient:
    return connection_service.ConnectionServiceClient()


@pytest.fixture(scope="session")
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="session")
def location() -> str:
    return "US"


@pytest.fixture(scope="session")
def database() -> str:
    return os.environ["MYSQL_DATABASE"]


@pytest.fixture(scope="session")
def cloud_sql_conn_name() -> str:
    return os.environ["MYSQL_INSTANCE"]


@pytest.fixture(scope="session")
def mysql_username() -> str:
    return os.environ["MYSQL_USER"]


@pytest.fixture(scope="session")
def mysql_password() -> str:
    return os.environ["MYSQL_PASSWORD"]
