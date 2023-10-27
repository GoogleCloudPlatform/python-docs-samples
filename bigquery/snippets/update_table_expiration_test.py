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

import datetime
import typing

import update_table_expiration  # type: ignore

if typing.TYPE_CHECKING:
    import pathlib

    import pytest


def test_update_table_expiration(
    capsys: "pytest.CaptureFixture[str]",
    table_id: str,
    tmp_path: "pathlib.Path",
) -> None:
    # This was not needed for function, only for test
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=5
    )

    update_table_expiration.update_table_expiration(table_id, expiration)

    out, _ = capsys.readouterr()
    assert "Updated" in out
    assert table_id in out
    assert str(expiration.day) in out
    assert str(expiration.month) in out
    assert str(expiration.year) in out
