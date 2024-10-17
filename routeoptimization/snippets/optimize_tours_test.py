# Copyright 2024 Google LLC
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


import optimize_tours


def test_call_sync_api(capsys: pytest.LogCaptureFixture) -> None:
    _, project_id = google.auth.default()
    got = optimize_tours.call_optimize_tours(project_id)

    for val in (got.routes, got.visits, got.metrics):
        assert val is not None
