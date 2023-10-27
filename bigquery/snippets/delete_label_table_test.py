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

import delete_label_table  # type: ignore

if typing.TYPE_CHECKING:
    import pytest


def test_delete_label_table(
    capsys: "pytest.CaptureFixture[str]",
    table_id: str,
) -> None:
    table = delete_label_table.delete_label_table(table_id, "color")

    out, _ = capsys.readouterr()
    assert "Deleted" in out
    assert "color" in out
    assert table_id in out
    assert table.labels is None or "color" not in table.labels
