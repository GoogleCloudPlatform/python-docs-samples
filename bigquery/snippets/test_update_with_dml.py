# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Iterator

from google.cloud import bigquery
import pytest

from conftest import prefixer
import update_with_dml


@pytest.fixture
def table_id(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
) -> Iterator[str]:
    table_id = f"{prefixer.create_prefix()}_update_with_dml"
    yield table_id
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    bigquery_client.delete_table(full_table_id, not_found_ok=True)


def test_update_with_dml(
    bigquery_client_patch: None, dataset_id: str, table_id: str
) -> None:
    override_values = {
        "dataset_id": dataset_id,
        "table_id": table_id,
    }
    num_rows = update_with_dml.run_sample(override_values=override_values)
    assert num_rows > 0
