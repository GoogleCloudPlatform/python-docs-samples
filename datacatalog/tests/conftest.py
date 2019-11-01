# Copyright 2019 Google LLC
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
import uuid

import pytest

import google.auth
from google.cloud import datacatalog_v1beta1


@pytest.fixture(scope="session")
def client(credentials):
    return datacatalog_v1beta1.DataCatalogClient(credentials=credentials)


@pytest.fixture(scope="session")
def default_credentials():
    return google.auth.default()


@pytest.fixture(scope="session")
def credentials(default_credentials):
    return default_credentials[0]


@pytest.fixture(scope="session")
def project_id(default_credentials):
    return default_credentials[1]


@pytest.fixture
def random_entry_group_id(client, project_id):
    now = datetime.datetime.now()
    random_entry_group_id = "example_entry_group_{}_{}".format(
        now.strftime("%Y%m%d%H%M%S"), uuid.uuid4().hex[:8]
    )
    yield random_entry_group_id
    entry_group_name = datacatalog_v1beta1.DataCatalogClient.entry_group_path(
        project_id, "us-central1", random_entry_group_id
    )
    client.delete_entry_group(entry_group_name)
