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

import sync_api_with_long_timeout


def test_long_timeout(capsys: pytest.LogCaptureFixture) -> None:
    request_file_name = "resources/sync_request.json"
    _, project_id = google.auth.default()
    sync_api_with_long_timeout.long_timeout(request_file_name, project_id)
    out, _ = capsys.readouterr()

    expected_strings = ["routes", "visits", "transitions", "metrics"]
    for expected_string in expected_strings:
        assert expected_string in out
