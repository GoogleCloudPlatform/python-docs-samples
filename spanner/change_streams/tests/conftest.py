# Copyright 2026 Google LLC
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

"""Shared live-test configuration for Cloud Spanner Change Streams Samples."""

import os

import pytest

LIVE_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LIVE_INSTANCE_ID = os.environ.get("SPANNER_INSTANCE_ID", "")
LIVE_DATABASE_ID = os.environ.get("SPANNER_DATABASE_ID", "")

if os.environ.get("RUN_INTEGRATION_TESTS") == "true" and (
    not LIVE_PROJECT_ID or not LIVE_INSTANCE_ID or not LIVE_DATABASE_ID
):
    raise RuntimeError(
        "Set GOOGLE_CLOUD_PROJECT, SPANNER_INSTANCE_ID, and "
        "SPANNER_DATABASE_ID when RUN_INTEGRATION_TESTS=true."
    )

live_only = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION_TESTS") != "true",
    reason="Set RUN_INTEGRATION_TESTS=true to run integration tests.",
)
