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
import uuid

from google.api_core import exceptions
from google.cloud import bigquery
import pytest

import materialized_view


def temp_suffix():
    return str(uuid.uuid4()).replace("-", "_")


@pytest.fixture(scope="module")
def bigquery_client():
    bigquery_client = bigquery.Client()
    return bigquery_client


@pytest.fixture(autouse=True)
def bigquery_client_patch(monkeypatch, bigquery_client):
    monkeypatch.setattr(bigquery, "Client", lambda: bigquery_client)


@pytest.fixture(scope="module")
def project_id(bigquery_client):
    return bigquery_client.project


@pytest.fixture(scope="module")
def dataset_id(bigquery_client):
    dataset_id = f"mvdataset_{temp_suffix()}"
    bigquery_client.create_dataset(dataset_id)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="module")
def base_table_id(bigquery_client, project_id, dataset_id):
    base_table_id = f"{project_id}.{dataset_id}.base_{temp_suffix()}"
    # Schema from materialized views guide:
    # https://cloud.google.com/bigquery/docs/materialized-views#create
    base_table = bigquery.Table(base_table_id)
    base_table.schema = [
        bigquery.SchemaField("product_id", bigquery.SqlTypeNames.INT64),
        bigquery.SchemaField("clicks", bigquery.SqlTypeNames.INT64),
    ]
    bigquery_client.create_table(base_table)
    yield base_table_id
    bigquery_client.delete_table(base_table_id)


@pytest.fixture(scope="module")
def view_id(bigquery_client, project_id, dataset_id):
    view_id = f"{project_id}.{dataset_id}.mview_{temp_suffix()}"
    yield view_id
    bigquery_client.delete_table(view_id, not_found_ok=True)


def test_materialized_view(capsys, bigquery_client, base_table_id, view_id):
    override_values = {
        "base_table_id": base_table_id,
        "view_id": view_id,
    }
    view = materialized_view.create_materialized_view(override_values)
    assert base_table_id in view.mview_query
    out, _ = capsys.readouterr()
    assert view_id in out

    view = materialized_view.update_materialized_view(override_values)
    assert view.mview_enable_refresh
    assert view.mview_refresh_interval == datetime.timedelta(hours=1)
    out, _ = capsys.readouterr()
    assert view_id in out

    materialized_view.delete_materialized_view(override_values)
    with pytest.raises(exceptions.NotFound):
        bigquery_client.get_table(view_id)
