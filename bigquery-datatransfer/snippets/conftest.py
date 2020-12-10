# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.exceptions
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_datatransfer
import pytest


@pytest.fixture(scope="session")
def default_credentials():
    return google.auth.default(["https://www.googleapis.com/auth/cloud-platform"])


@pytest.fixture(scope="session")
def project_id(default_credentials):
    _, project_id = default_credentials
    return project_id


@pytest.fixture(scope="session")
def bigquery_client(default_credentials):
    credentials, project_id = default_credentials
    return bigquery.Client(credentials=credentials, project=project_id)


@pytest.fixture(scope="session")
def transfer_client(default_credentials):
    credentials, _ = default_credentials
    return bigquery_datatransfer.DataTransferServiceClient(credentials=credentials)


@pytest.fixture
def to_delete_configs(transfer_client):
    to_delete = []
    yield to_delete
    for config_name in to_delete:
        try:
            transfer_client.delete_transfer_config(name=config_name)
        except google.api_core.exceptions.GoogleAPICallError:
            pass
