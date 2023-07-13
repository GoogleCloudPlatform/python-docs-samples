# Copyright 2019 Google LLC
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

import pytest

from .. import copy_table

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def test_copy_table(
    capsys: "pytest.CaptureFixture[str]",
    table_with_data_id: str,
    random_table_id: str,
    client: "bigquery.Client",
) -> None:
    copy_table.copy_table(table_with_data_id, random_table_id)
    out, err = capsys.readouterr()
    assert "A copy of the table created." in out
    assert (
        client.get_table(random_table_id).num_rows
        == client.get_table(table_with_data_id).num_rows
    )
