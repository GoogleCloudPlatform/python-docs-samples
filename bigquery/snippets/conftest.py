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

from typing import Iterator

from google.cloud import bigquery
import pytest
import test_utils.prefixer

prefixer = test_utils.prefixer.Prefixer("python-bigquery", "samples/snippets")


@pytest.fixture(scope="session", autouse=True)
def cleanup_datasets(bigquery_client: bigquery.Client) -> None:
    for dataset in bigquery_client.list_datasets():
        if prefixer.should_cleanup(dataset.dataset_id):
            bigquery_client.delete_dataset(
                dataset, delete_contents=True, not_found_ok=True
            )


@pytest.fixture(scope="session")
def bigquery_client() -> bigquery.Client:
    bigquery_client = bigquery.Client()
    return bigquery_client


@pytest.fixture(scope="session")
def project_id(bigquery_client: bigquery.Client) -> str:
    return bigquery_client.project


@pytest.fixture(scope="session")
def dataset_id(bigquery_client: bigquery.Client, project_id: str) -> Iterator[str]:
    dataset_id = prefixer.create_prefix()
    full_dataset_id = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(full_dataset_id)
    bigquery_client.create_dataset(dataset)
    yield dataset_id
    bigquery_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture
def table_id(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
) -> Iterator[str]:
    table_id = prefixer.create_prefix()
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    table = bigquery.Table(
        full_table_id, schema=[bigquery.SchemaField("string_col", "STRING")]
    )
    bigquery_client.create_table(table)
    yield full_table_id
    bigquery_client.delete_table(table, not_found_ok=True)


@pytest.fixture(scope="session")
def entity_id(bigquery_client: bigquery.Client, dataset_id: str) -> str:
    return "cloud-developer-relations@google.com"


@pytest.fixture(scope="session")
def dataset_id_us_east1(
    bigquery_client: bigquery.Client,
    project_id: str,
) -> Iterator[str]:
    dataset_id = prefixer.create_prefix()
    full_dataset_id = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(full_dataset_id)
    dataset.location = "us-east1"
    bigquery_client.create_dataset(dataset)
    yield dataset_id
    bigquery_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="session")
def table_id_us_east1(
    bigquery_client: bigquery.Client, project_id: str, dataset_id_us_east1: str
) -> Iterator[str]:
    table_id = prefixer.create_prefix()
    full_table_id = f"{project_id}.{dataset_id_us_east1}.{table_id}"
    table = bigquery.Table(
        full_table_id, schema=[bigquery.SchemaField("string_col", "STRING")]
    )
    bigquery_client.create_table(table)
    yield full_table_id
    bigquery_client.delete_table(table, not_found_ok=True)


@pytest.fixture
def random_table_id(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
) -> Iterator[str]:
    """Create a new table ID each time, so random_table_id can be used as
    target for load jobs.
    """
    random_table_id = prefixer.create_prefix()
    full_table_id = f"{project_id}.{dataset_id}.{random_table_id}"
    yield full_table_id
    bigquery_client.delete_table(full_table_id, not_found_ok=True)


@pytest.fixture
def bigquery_client_patch(
    monkeypatch: pytest.MonkeyPatch, bigquery_client: bigquery.Client
) -> None:
    monkeypatch.setattr(bigquery, "Client", lambda: bigquery_client)
