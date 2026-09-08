# Copyright 2019 Google LLC
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

import typing

import pytest

from .. import load_table_dataframe

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


pandas = pytest.importorskip("pandas")
pyarrow = pytest.importorskip("pyarrow")


def test_load_table_dataframe(
    capsys: pytest.CaptureFixture[str],
    client: "bigquery.Client",
    random_table_id: str,
) -> None:
    table = load_table_dataframe.load_table_dataframe(random_table_id)
    out, _ = capsys.readouterr()
    expected_column_names = [
        "wikidata_id",
        "title",
        "release_year",
        "length_minutes",
        "release_date",
        "dvd_release",
    ]
    assert "Loaded 4 rows and {} columns".format(len(expected_column_names)) in out

    column_names = [field.name for field in table.schema]
    assert column_names == expected_column_names
    column_types = [field.field_type for field in table.schema]
    assert column_types == [
        "STRING",
        "STRING",
        "INTEGER",
        "FLOAT",
        "TIMESTAMP",
        "DATETIME",
    ]

    df = client.list_rows(table).to_dataframe()
    df.sort_values("release_year", inplace=True)
    assert df["title"].tolist() == [
        "And Now for Something Completely Different",
        "Monty Python and the Holy Grail",
        "Life of Brian",
        "The Meaning of Life",
    ]
    assert df["release_year"].tolist() == [1971, 1975, 1979, 1983]
    assert df["length_minutes"].tolist() == [88.0, 91.5, 94.25, 112.5]
    assert df["release_date"].tolist() == [
        pandas.Timestamp("1971-09-28T22:59:07+00:00"),
        pandas.Timestamp("1975-04-09T22:59:02+00:00"),
        pandas.Timestamp("1979-08-18T03:59:05+00:00"),
        pandas.Timestamp("1983-05-09T11:00:00+00:00"),
    ]
    assert df["dvd_release"].tolist() == [
        pandas.Timestamp("2003-10-22T10:00:00"),
        pandas.Timestamp("2002-07-16T09:00:00"),
        pandas.Timestamp("2008-01-14T08:00:00"),
        pandas.Timestamp("2002-01-22T07:00:00"),
    ]
    assert df["wikidata_id"].tolist() == ["Q16403", "Q25043", "Q24953", "Q24980"]
