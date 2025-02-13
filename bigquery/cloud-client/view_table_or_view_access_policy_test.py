# Copyright 2025 Google LLC
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

# pylint: disable=redefined-outer-name

import os

from google.api_core.exceptions import NotFound
from google.api_core.iam import Policy
from google.cloud import bigquery
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.table import Table

import pytest

from conftest import prefixer

from view_table_or_view_access_policy import view_table_or_view_access_policy

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
PREFIX = prefixer.create_prefix()
DATASET_ID = f"{PREFIX}_view_access_policies"

TABLE_NAME = f"{PREFIX}_view_access_policies_table"
FULL_TABLE_NAME = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

VIEW_NAME = f"{PREFIX}_view_access_policies_view"
FULL_VIEW_NAME = f"{PROJECT_ID}.{DATASET_ID}.{VIEW_NAME}"

TABLE_FOR_VIEW_NAME = f"{PREFIX}_view_access_policies_table_for_view"
TABLE_FOR_VIEW_FULL_NAME = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_FOR_VIEW_NAME}"


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture(scope="module")
def dataset(client: bigquery.Client) -> Dataset:
    dataset = client.create_dataset(DATASET_ID)
    yield dataset
    client.delete_dataset(dataset, delete_contents=True)
    try:
        client.get_dataset(DATASET_ID)
    except NotFound:
        return

    pytest.fail(f"The dataset '{DATASET_ID}' was not deleted.")


def create_table(
    client: bigquery.Client,
    full_table_name: str
) -> None:
    sample_schema = [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    ]

    table = bigquery.Table(full_table_name, schema=sample_schema)
    client.create_table(table)

    return table


@pytest.fixture()
def table(client: bigquery.Client) -> Table:
    return create_table(client, FULL_TABLE_NAME)


@pytest.fixture()
def table_for_view(client: bigquery.Client) -> Table:
    return create_table(client, TABLE_FOR_VIEW_FULL_NAME)


@pytest.fixture()
def view(client: bigquery.Client, table_for_view: str) -> str:
    view = bigquery.Table(FULL_VIEW_NAME)
    # 'table_for_view' will inject the full view name,
    # with project_id and dataset_id
    view.view_query = f"SELECT * FROM `{table_for_view}`"
    view = client.create_table(view)
    return view


def test_view_dataset_access_policies_with_table(
    dataset: Dataset,
    table: Table,
) -> None:
    policy: Policy = view_table_or_view_access_policy(PROJECT_ID, dataset.dataset_id, table.table_id)

    assert policy.etag == "ACAB"  # An empty policy


def test_view_dataset_access_policies_with_view(
    dataset: Dataset,
    view: Table,
) -> None:
    print(view)
    policy: Policy = view_table_or_view_access_policy(PROJECT_ID, dataset.dataset_id, view.table_id)

    assert policy.etag == "ACAB"  # An empty policy
