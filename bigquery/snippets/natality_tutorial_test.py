# Copyright 2018 Google Inc. All Rights Reserved.
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

from typing import Iterator, List

from google.cloud import bigquery
import pytest

import natality_tutorial  # type: ignore
from conftest import prefixer  # type: ignore


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture
def datasets_to_delete(client: bigquery.Client) -> Iterator[List[str]]:
    doomed: List[str] = []
    yield doomed
    for item in doomed:
        client.delete_dataset(item, delete_contents=True)


def test_natality_tutorial(
    client: bigquery.Client, datasets_to_delete: List[str]
) -> None:
    override_values = {"dataset_id": f"{prefixer.create_prefix()}_natality_tutorial"}
    datasets_to_delete.append(override_values["dataset_id"])

    natality_tutorial.run_natality_tutorial(override_values)

    table_ref = "{}.{}.{}".format(
        client.project, override_values["dataset_id"], "regression_input"
    )
    table = client.get_table(table_ref)
    assert table.num_rows > 0
