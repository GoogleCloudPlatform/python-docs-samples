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

import pathlib
import random

from google.cloud import bigquery
import pytest

from . import append_rows_pending

DIR = pathlib.Path(__file__).parent


regions = ["US", "non-US"]


@pytest.fixture(params=regions)
def sample_data_table(
    request: pytest.FixtureRequest,
    bigquery_client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    dataset_id_non_us: str,
) -> str:
    dataset = dataset_id
    if request.param != "US":
        dataset = dataset_id_non_us
    schema = bigquery_client.schema_from_json(str(DIR / "customer_record_schema.json"))
    table_id = f"append_rows_proto2_{random.randrange(10000)}"
    full_table_id = f"{project_id}.{dataset}.{table_id}"
    table = bigquery.Table(full_table_id, schema=schema)
    table = bigquery_client.create_table(table, exists_ok=True)
    yield full_table_id
    bigquery_client.delete_table(table, not_found_ok=True)


def test_append_rows_pending(
    capsys: pytest.CaptureFixture,
    bigquery_client: bigquery.Client,
    sample_data_table: str,
) -> None:
    project_id, dataset_id, table_id = sample_data_table.split(".")
    append_rows_pending.append_rows_pending(
        project_id=project_id, dataset_id=dataset_id, table_id=table_id
    )
    out, _ = capsys.readouterr()
    assert "have been committed" in out

    rows = bigquery_client.query(
        f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    ).result()
    row_items = [
        # Convert to sorted tuple of items to more easily search for expected rows.
        tuple(sorted(row.items()))
        for row in rows
    ]

    assert (("customer_name", "Alice"), ("row_num", 1)) in row_items
    assert (("customer_name", "Bob"), ("row_num", 2)) in row_items
    assert (("customer_name", "Charles"), ("row_num", 3)) in row_items
