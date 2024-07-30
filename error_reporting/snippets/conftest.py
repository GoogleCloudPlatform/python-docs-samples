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
from google.cloud import errorreporting_v1beta1
from google.cloud.errorreporting_v1beta1.types import error_stats_service
import pytest

PROJECT = google.auth.default()[1]


@pytest.fixture(scope="session")
def ess_client():
    service = errorreporting_v1beta1.ErrorStatsServiceClient()
    try:
        yield service
    finally:
        req = error_stats_service.DeleteEventsRequest()
        req.project_name = f"projects/{PROJECT}"
        data = service.delete_events(req)
        assert not data
