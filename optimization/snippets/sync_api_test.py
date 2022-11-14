# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.auth
import pytest


import sync_api


def test_call_sync_api(capsys: pytest.LogCaptureFixture) -> None:
    _, project_id = google.auth.default()
    sync_api.call_sync_api(project_id)
    out, _ = capsys.readouterr()

    expected_strings = ["routes", "visits", "transitions", "metrics"]
    for expected_string in expected_strings:
        assert expected_string in out
