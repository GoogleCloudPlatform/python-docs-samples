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

import os
from typing import Iterator, List

from google.cloud import bigquery
import pytest

from conftest import prefixer

from view_table_or_view_access_policy import view_table_or_view_access_policy

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = f"{prefixer.create_prefix()}_view_table_or_view_access_policies"
TABLE_NAME = f"{prefixer.create_prefix()}_view_table_or_view_access_policies_table"
VIEW_NAME = f"{prefixer.create_prefix()}_view_table_or_view_access_policies_view"
TABLE_NAME_FOR_VIEW = f"{prefixer.create_prefix()}_view_table_or_view_access_policies_table_for_view"


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture()
def create_dataset(client: bigquery.Client):
    client.create_dataset(DATASET_ID)


@pytest.fixture()
def create_table(client: bigquery.Client):
    schema = [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    ]

    full_table_name = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

    table = bigquery.Table(full_table_name, schema=schema)
    table = client.create_table(table)


@pytest.fixture()
def create_table_for_view(client: bigquery.Client):
    schema = [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    ]

    full_table_name = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME_FOR_VIEW}"

    table = bigquery.Table(full_table_name, schema=schema)
    table = client.create_table(table)


@pytest.fixture()
def create_view(client: bigquery.Client):
    # Note: The view requires the table to be created first
    view_id = f"{PROJECT_ID}.{DATASET_ID}.{VIEW_NAME}"
    source_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME_FOR_VIEW}"

    view = bigquery.Table(view_id)

    view.view_query = f"SELECT * FROM `{source_id}`"

    view = client.create_table(view)


@pytest.fixture
def datasets_to_delete(client: bigquery.Client) -> Iterator[List[str]]:
    # Note: Table and View will be deleted along with datasets
    datasets: List[str] = []
    yield datasets
    for item in datasets:
        client.delete_dataset(item, delete_contents=True)


def test_view_dataset_access_policies_with_table(
    capsys: "pytest.CaptureFixture[str]",
    client: bigquery.Client,
    create_dataset: None,
    create_table: None,
    datasets_to_delete: List[str],
) -> None:
    override_values = {"dataset_id": DATASET_ID, "resource_name": TABLE_NAME}
    datasets_to_delete.append(override_values["dataset_id"])

    view_table_or_view_access_policy(override_values)
    out, _ = capsys.readouterr()
    assert f"Details for Access entry 0 in Table or View '{TABLE_NAME}'" in out


def test_view_dataset_access_policies_with_view(
    capsys: "pytest.CaptureFixture[str]",
    client: bigquery.Client,
    create_dataset: None,
    create_table_for_view: None,
    create_view: None,    datasets_to_delete: List[str],
) -> None:
    override_values = {"dataset_id": DATASET_ID, "resource_name": VIEW_NAME}
    datasets_to_delete.append(override_values["dataset_id"])

    view_table_or_view_access_policy(override_values)
    out, _ = capsys.readouterr()
    assert f"Details for Access entry 0 in Table or View '{VIEW_NAME}'" in out
