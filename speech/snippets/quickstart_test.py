# Copyright 2016 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from google.api_core.retry import Retry

import pytest

import quickstart


@Retry()
def test_quickstart(capsys: pytest.CaptureFixture) -> None:
    result = quickstart.run_quickstart()
    out, _ = capsys.readouterr()
    assert "Transcript: how old is the Brooklyn Bridge" in out
    assert result is not None
