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

import get_table_make_schema

if typing.TYPE_CHECKING:
    import pathlib

    import pytest


def test_get_table_make_schema(
    capsys: "pytest.CaptureFixture[str]",
    table_id: str,
    tmp_path: "pathlib.Path",
) -> None:
    schema_path = str(tmp_path / "test_schema.json")

    get_table_make_schema.get_table_make_schema(table_id, schema_path)

    out, _ = capsys.readouterr()
    assert "Got table" in out
    assert table_id in out
