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

from .. import delete_table

if typing.TYPE_CHECKING:
    import pytest


def test_delete_table(capsys: "pytest.CaptureFixture[str]", table_id: str) -> None:

    delete_table.delete_table(table_id)
    out, err = capsys.readouterr()
    assert "Deleted table '{}'.".format(table_id) in out
