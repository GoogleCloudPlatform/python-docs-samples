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

from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.cloud.bigquery.dataset import AccessEntry, Dataset
import pytest

from conftest import prefixer
from view_dataset_access_policy import view_dataset_access_policy

DATASET_ID = f"{prefixer.create_prefix()}_view_dataset_access_policies"


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture()
def dataset(client: bigquery.Client) -> Dataset:
    dataset = client.create_dataset(DATASET_ID)
    yield dataset
    client.delete_dataset(dataset, delete_contents=True)
    try:
        client.get_dataset(DATASET_ID)
    except NotFound:
        return

    pytest.fail(f"The dataset '{DATASET_ID}' was not deleted.")


def test_view_dataset_access_policies(
    client: bigquery.Client,
    dataset: Dataset,
) -> None:
    access_policy: list[AccessEntry] = view_dataset_access_policy(dataset.dataset_id)

    assert access_policy
