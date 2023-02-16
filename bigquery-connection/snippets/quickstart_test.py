# Copyright 2021 Google LLC
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

import pytest

from . import quickstart


@pytest.mark.parametrize("transport", ["grpc", "rest"])
def test_quickstart(
    capsys: pytest.CaptureFixture, project_id: str, location: str, transport: str
) -> None:
    quickstart.main(project_id, location, transport)
    out, _ = capsys.readouterr()
    assert "List of connections in project" in out
