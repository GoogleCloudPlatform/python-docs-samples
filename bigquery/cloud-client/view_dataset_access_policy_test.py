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

from collections.abc import Iterator

from google.cloud import bigquery
import pytest

from conftest import prefixer

from view_dataset_access_policy import view_dataset_access_policy

DATASET_ID = f"{prefixer.create_prefix()}_view_dataset_access_policies"


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture()
def create_dataset(client: bigquery.Client):
    client.create_dataset(DATASET_ID)


@pytest.fixture
def datasets_to_delete(client: bigquery.Client) -> Iterator[list[str]]:
    datasets: list[str] = []
    yield datasets
    for item in datasets:
        client.delete_dataset(item, delete_contents=True)


def test_view_dataset_access_policies(
    capsys: "pytest.CaptureFixture[str]",
    client: bigquery.Client,
    create_dataset: None,
    datasets_to_delete: list[str],
) -> None:
    view_dataset_access_policy(dataset_id=DATASET_ID)
    out, _ = capsys.readouterr()
    assert "AccessEntry:" in out
