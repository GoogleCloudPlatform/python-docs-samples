# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import list_info_types as metadata

import pytest


def test_fetch_info_types(capsys: pytest.CaptureFixture) -> None:
    metadata.list_info_types()

    out, _ = capsys.readouterr()
    assert "EMAIL_ADDRESS" in out
