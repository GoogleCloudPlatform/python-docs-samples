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

import create_table_cmek  # type: ignore

if typing.TYPE_CHECKING:
    import pytest


def test_create_table(
    capsys: "pytest.CaptureFixture[str]",
    random_table_id: str,
) -> None:
    kms_key_name = (
        "projects/cloud-samples-tests/locations/us/keyRings/test/cryptoKeys/test"
    )

    create_table_cmek.create_table_cmek(random_table_id, kms_key_name)

    out, _ = capsys.readouterr()
    assert "Created" in out
    assert random_table_id in out
    assert kms_key_name in out
