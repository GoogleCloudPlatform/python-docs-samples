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


def temp_suffix() -> str:
    now = datetime.datetime.now()
    return f"{now.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def bigquery_client() -> bigquery.Client:
    bigquery_client = bigquery.Client()
    return bigquery_client


@pytest.fixture(scope="session")
def project_id(bigquery_client: bigquery.Client) -> str:
    return bigquery_client.project


@pytest.fixture
def dataset_id(bigquery_client: bigquery.Client) -> Iterator[str]:
    dataset_id = f"geography_{temp_suffix()}"
    bigquery_client.create_dataset(dataset_id)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture
def table_id(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
) -> Iterator[str]:
    table_id = f"{project_id}.{dataset_id}.geography_{temp_suffix()}"
    table = bigquery.Table(table_id)
    table.schema = [
        bigquery.SchemaField("geo", bigquery.SqlTypeNames.GEOGRAPHY),
    ]
    bigquery_client.create_table(table)
    yield table_id
    bigquery_client.delete_table(table_id)
