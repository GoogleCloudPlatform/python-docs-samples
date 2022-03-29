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

import datetime
import decimal
import pathlib
import random

from google.cloud import bigquery
import pytest

from . import append_rows_proto2


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
    schema = bigquery_client.schema_from_json(str(DIR / "sample_data_schema.json"))
    table_id = f"append_rows_proto2_{random.randrange(10000)}"
    full_table_id = f"{project_id}.{dataset}.{table_id}"
    table = bigquery.Table(full_table_id, schema=schema)
    table = bigquery_client.create_table(table, exists_ok=True)
    yield full_table_id
    bigquery_client.delete_table(table, not_found_ok=True)


def test_append_rows_proto2(
    capsys: pytest.CaptureFixture,
    bigquery_client: bigquery.Client,
    sample_data_table: str,
):
    project_id, dataset_id, table_id = sample_data_table.split(".")
    append_rows_proto2.append_rows_proto2(
        project_id=project_id, dataset_id=dataset_id, table_id=table_id
    )
    out, _ = capsys.readouterr()
    assert "have been committed" in out

    rows = bigquery_client.query(
        f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    ).result()
    row_items = [
        # Convert to sorted tuple of items, omitting NULL values, to make
        # searching for expected rows easier.
        tuple(
            sorted(
                item for item in row.items() if item[1] is not None and item[1] != []
            )
        )
        for row in rows
    ]

    assert (
        ("bool_col", True),
        ("bytes_col", b"Hello, World!"),
        ("float64_col", float("+inf")),
        ("int64_col", 123),
        ("row_num", 1),
        ("string_col", "Howdy!"),
    ) in row_items
    assert (("bool_col", False), ("row_num", 2)) in row_items
    assert (("bytes_col", b"See you later!"), ("row_num", 3)) in row_items
    assert (("float64_col", 1000000.125), ("row_num", 4)) in row_items
    assert (("int64_col", 67000), ("row_num", 5)) in row_items
    assert (("row_num", 6), ("string_col", "Auf Wiedersehen!")) in row_items
    assert (("date_col", datetime.date(2021, 8, 12)), ("row_num", 7)) in row_items
    assert (
        ("datetime_col", datetime.datetime(2021, 8, 12, 9, 46, 23, 987456)),
        ("row_num", 8),
    ) in row_items
    assert (
        ("geography_col", "POINT(-122.347222 47.651111)"),
        ("row_num", 9),
    ) in row_items
    assert (
        ("bignumeric_col", decimal.Decimal("-1.234567891011121314151617181920e+16")),
        ("numeric_col", decimal.Decimal("1.23456789101112e+6")),
        ("row_num", 10),
    ) in row_items
    assert (
        ("row_num", 11),
        ("time_col", datetime.time(11, 7, 48, 123456)),
    ) in row_items
    assert (
        ("row_num", 12),
        (
            "timestamp_col",
            datetime.datetime(
                2021, 8, 12, 16, 11, 22, 987654, tzinfo=datetime.timezone.utc
            ),
        ),
    ) in row_items
    assert (("int64_list", [1, 2, 3]), ("row_num", 13)) in row_items
    assert (
        ("row_num", 14),
        ("struct_col", {"sub_int_col": 7}),
    ) in row_items
    assert (
        ("row_num", 15),
        (
            "struct_list",
            [{"sub_int_col": -1}, {"sub_int_col": -2}, {"sub_int_col": -3}],
        ),
    ) in row_items
