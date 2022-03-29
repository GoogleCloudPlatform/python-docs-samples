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

from .. import update_dataset_default_partition_expiration

if typing.TYPE_CHECKING:
    import pytest


def test_update_dataset_default_partition_expiration(
    capsys: "pytest.CaptureFixture[str]", dataset_id: str
) -> None:

    ninety_days_ms = 90 * 24 * 60 * 60 * 1000  # in milliseconds

    update_dataset_default_partition_expiration.update_dataset_default_partition_expiration(
        dataset_id
    )
    out, _ = capsys.readouterr()
    assert (
        "Updated dataset {} with new default partition expiration {}".format(
            dataset_id, ninety_days_ms
        )
        in out
    )
