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

from google.api_core.retry import Retry
import google.auth


import optimize_tours


@Retry
def test_call_sync_api() -> None:
    _, project_id = google.auth.default()
    got = optimize_tours.call_optimize_tours(project_id)

    assert len(got.routes) > 0
    assert len(got.routes[0].visits) > 0
    assert got.metrics is not None
