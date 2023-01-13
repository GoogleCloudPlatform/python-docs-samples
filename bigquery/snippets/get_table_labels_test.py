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

import get_table_labels

if typing.TYPE_CHECKING:
    import pytest


def test_get_table_labels(
    capsys: "pytest.CaptureFixture[str]",
    table_id: str,
    bigquery_client: bigquery.Client,
) -> None:
    table = bigquery_client.get_table(table_id)
    table.labels = {"color": "green"}
    bigquery_client.update_table(table, ["labels"])

    get_table_labels.get_table_labels(table_id)

    out, _ = capsys.readouterr()
    assert table_id in out
    assert "color" in out


def test_get_table_labels_no_label(
    capsys: "pytest.CaptureFixture[str]",
    table_id: str,
) -> None:

    get_table_labels.get_table_labels(table_id)

    out, _ = capsys.readouterr()
    assert "no labels defined" in out
    assert table_id in out
