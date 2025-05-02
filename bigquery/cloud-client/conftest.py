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

from google.cloud import bigquery
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.table import Table

import pytest
import test_utils.prefixer

prefixer = test_utils.prefixer.Prefixer("python-docs-samples", "bigquery/cloud-client")

PREFIX = prefixer.create_prefix()
ENTITY_ID = "cloud-developer-relations@google.com"  # Group account
DATASET_ID = f"{PREFIX}_access_policies_dataset"
TABLE_NAME = f"{PREFIX}_access_policies_table"
VIEW_NAME = f"{PREFIX}_access_policies_view"


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture(scope="module")
def project_id(client: bigquery.Client) -> str:
    return client.project


@pytest.fixture(scope="module")
def entity_id() -> str:
    return ENTITY_ID


@pytest.fixture(scope="module")
def dataset(client: bigquery.Client) -> Dataset:
    dataset = client.create_dataset(DATASET_ID)
    yield dataset
    client.delete_dataset(dataset, delete_contents=True)


@pytest.fixture(scope="module")
def table(client: bigquery.Client, project_id: str) -> Table:
    FULL_TABLE_NAME = f"{project_id}.{DATASET_ID}.{TABLE_NAME}"

    sample_schema = [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    ]

    table = bigquery.Table(FULL_TABLE_NAME, schema=sample_schema)
    client.create_table(table)

    return table


@pytest.fixture()
def view(client: bigquery.Client, project_id: str, table: str) -> str:
    FULL_VIEW_NAME = f"{project_id}.{DATASET_ID}.{VIEW_NAME}"
    view = bigquery.Table(FULL_VIEW_NAME)

    # f"{table}" will inject the full table name,
    # with project_id and dataset_id, as required by create_table()
    view.view_query = f"SELECT * FROM `{table}`"
    view = client.create_table(view)
    return view
