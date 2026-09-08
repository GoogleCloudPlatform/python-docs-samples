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

import datetime
from typing import Iterator
import uuid

from google.cloud import bigquery
import pytest

import view  # type: ignore
from conftest import prefixer  # type: ignore


def temp_suffix() -> str:
    now = datetime.datetime.now()
    return f"{now.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"


@pytest.fixture(autouse=True)
def bigquery_client_patch(
    monkeypatch: pytest.MonkeyPatch, bigquery_client: bigquery.Client
) -> None:
    monkeypatch.setattr(bigquery, "Client", lambda: bigquery_client)


@pytest.fixture(scope="module")
def view_dataset_id(bigquery_client: bigquery.Client, project_id: str) -> Iterator[str]:
    dataset_id = f"{project_id}.view_{temp_suffix()}"
    bigquery_client.create_dataset(dataset_id)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="module")
def view_id(bigquery_client: bigquery.Client, view_dataset_id: str) -> Iterator[str]:
    view_id = f"{view_dataset_id}.my_view"
    yield view_id
    bigquery_client.delete_table(view_id, not_found_ok=True)


@pytest.fixture(scope="module")
def source_dataset_id(
    bigquery_client: bigquery.Client, project_id: str
) -> Iterator[str]:
    dataset_id = f"{prefixer.create_prefix()}_view"
    bigquery_client.create_dataset(dataset_id)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="module")
def source_table_id(
    bigquery_client: bigquery.Client, source_dataset_id: str
) -> Iterator[str]:
    source_table_id = f"{source_dataset_id}.us_states"
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("post_abbr", "STRING"),
        ],
        skip_leading_rows=1,
    )
    load_job = bigquery_client.load_table_from_uri(
        "gs://cloud-samples-data/bigquery/us-states/us-states.csv",
        source_table_id,
        job_config=job_config,
    )
    load_job.result()
    yield source_table_id
    bigquery_client.delete_table(source_table_id, not_found_ok=True)


def test_view(
    capsys: pytest.CaptureFixture[str],
    view_id: str,
    view_dataset_id: str,
    source_table_id: str,
    source_dataset_id: str,
) -> None:
    override_values = {
        "view_id": view_id,
        "source_id": source_table_id,
    }
    got = view.create_view(override_values)
    assert source_table_id in got.view_query
    out, _ = capsys.readouterr()
    assert view_id in out

    got = view.get_view(override_values)
    assert source_table_id in got.view_query
    assert "'W%'" in got.view_query
    out, _ = capsys.readouterr()
    assert view_id in out
    assert source_table_id in out
    assert "'W%'" in out

    got = view.update_view(override_values)
    assert source_table_id in got.view_query
    assert "'M%'" in got.view_query
    out, _ = capsys.readouterr()
    assert view_id in out

    project_id, dataset_id, table_id = view_id.split(".")
    overrides: view.OverridesDict = {
        "view_dataset_id": view_dataset_id,
        "source_dataset_id": source_dataset_id,
        "view_reference": {
            "projectId": project_id,
            "datasetId": dataset_id,
            "tableId": table_id,
        },
    }
    view_dataset, source_dataset = view.grant_access(overrides)
    assert len(view_dataset.access_entries) != 0
    assert len(source_dataset.access_entries) != 0
    out, _ = capsys.readouterr()
    assert "example-analyst-group@google.com" in out
    assert table_id in out
