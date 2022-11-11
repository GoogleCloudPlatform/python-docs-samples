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
from google.cloud import optimization_v1
import pytest

import get_operation


@pytest.fixture(scope="function")
def operation_id() -> str:
    fleet_routing_client = optimization_v1.FleetRoutingClient()

    _, project_id = google.auth.default()
    fleet_routing_request = {"parent": f"projects/{project_id}"}

    # Make the request
    operation = fleet_routing_client.batch_optimize_tours(fleet_routing_request)

    yield operation.operation.name


def test_get_operation_status(
    capsys: pytest.LogCaptureFixture, operation_id: str
) -> None:
    get_operation.get_operation(operation_id)
    out, _ = capsys.readouterr()
    assert "Operation details" in out
