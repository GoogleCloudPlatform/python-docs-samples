# Copyright 2022 Google LLC
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

import typing

from google.cloud import bigquery

import relax_column  # type: ignore

if typing.TYPE_CHECKING:
    import pytest


def test_relax_column(
    capsys: "pytest.CaptureFixture[str]",
    bigquery_client: bigquery.Client,
    random_table_id: str,
) -> None:
    table = bigquery.Table(
        random_table_id,
        schema=[
            bigquery.SchemaField("string_col", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("string_col2", "STRING", mode="REQUIRED"),
        ],
    )

    bigquery_client.create_table(table)
    table = relax_column.relax_column(random_table_id)

    out, _ = capsys.readouterr()

    assert all(field.mode == "NULLABLE" for field in table.schema)
    assert "REQUIRED" not in out
    assert "NULLABLE" in out
    assert random_table_id in out
