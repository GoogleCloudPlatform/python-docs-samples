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

import google.auth
from google.cloud import bigquery, datacatalog_v1
import pytest


def temp_suffix():
    now = datetime.datetime.now()
    return "{}_{}".format(now.strftime("%Y%m%d%H%M%S"), uuid.uuid4().hex[:8])


@pytest.fixture(scope="session")
def client(credentials):
    return datacatalog_v1.DataCatalogClient(credentials=credentials)


@pytest.fixture(scope="session")
def bigquery_client(credentials, project_id):
    return bigquery.Client(project=project_id, credentials=credentials)


@pytest.fixture(scope="session")
def default_credentials():
    return google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )


@pytest.fixture(scope="session")
def credentials(default_credentials):
    return default_credentials[0]


@pytest.fixture(scope="session")
def project_id(default_credentials):
    return default_credentials[1]


@pytest.fixture
def dataset_id(bigquery_client):
    dataset_id = f"python_data_catalog_sample_{temp_suffix()}"
    dataset = bigquery_client.create_dataset(dataset_id)
    yield dataset.dataset_id
    bigquery_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture
def table_id(bigquery_client, project_id, dataset_id):
    table_id = f"python_data_catalog_sample_{temp_suffix()}"
    table = bigquery.Table("{}.{}.{}".format(project_id, dataset_id, table_id))
    table = bigquery_client.create_table(table)
    yield table.table_id
    bigquery_client.delete_table(table, not_found_ok=True)


@pytest.fixture
def random_tag_template_id():
    random_tag_template_id = f"python_sample_{temp_suffix()}"
    yield random_tag_template_id
