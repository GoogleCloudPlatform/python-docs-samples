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
from typing import Iterator, List

from google.cloud import bigquery
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


@pytest.fixture()
def create_dataset(client: bigquery.Client):
    client.create_dataset(DATASET_ID)


def create_temporary_table(
        client: bigquery.Client,
        full_table_name: str):
    sample_schema = [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    ]

    table = bigquery.Table(full_table_name, schema=sample_schema)
    client.create_table(table)


@pytest.fixture()
def create_table(client: bigquery.Client):
    create_temporary_table(client, FULL_TABLE_NAME)


@pytest.fixture()
def create_table_for_view(client: bigquery.Client):
    create_temporary_table(client, TABLE_FOR_VIEW_FULL_NAME)


@pytest.fixture()
def create_view(client: bigquery.Client):
    # Note: The view requires the table to be created first
    view = bigquery.Table(FULL_VIEW_NAME)

    view.view_query = f"SELECT * FROM `{TABLE_FOR_VIEW_FULL_NAME}`"

    view = client.create_table(view)


@pytest.fixture
def datasets_to_delete(client: bigquery.Client) -> Iterator[List[str]]:
    datasets: List[str] = []
    yield datasets
    for item in datasets:
        # Note: Table and View will be deleted here
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
    assert f"Access Policy details for table or view '{TABLE_NAME}'." in out


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

    # Check that a policy was received
    assert f"Access Policy details for table or view '{VIEW_NAME}'." in out
