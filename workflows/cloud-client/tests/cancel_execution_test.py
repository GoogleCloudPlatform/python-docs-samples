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

from unittest import mock

from google.api_core import exceptions
from google.cloud.workflows import executions_v1
import pytest
from workflows_samples import cancel_execution

from . import conftest

PROJECT_ID = "test-project"
LOCATION_ID = "us-central1"
WORKFLOW_ID = "test-workflow"
EXECUTION_ID = "test-execution"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
WORKFLOW_NAME = f"{PARENT}/workflows/{WORKFLOW_ID}"
EXECUTION_NAME = f"{WORKFLOW_NAME}/executions/{EXECUTION_ID}"
EXECUTIONS_CLIENT = "google.cloud.workflows.executions_v1.ExecutionsClient"


@mock.patch(EXECUTIONS_CLIENT)
def test_cancel_execution_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.cancel_execution.return_value = executions_v1.Execution(
        name=EXECUTION_NAME, state=executions_v1.Execution.State.CANCELLED
    )

    cancel_execution.cancel_execution(
        PROJECT_ID, LOCATION_ID, WORKFLOW_ID, EXECUTION_ID
    )

    assert client.cancel_execution.call_args.kwargs["name"] == EXECUTION_NAME
    out, err = capsys.readouterr()
    assert "State: CANCELLED" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected",
    [
        (
            exceptions.NotFound("test detail"),
            "error: execution 'test-execution' not found",
        ),
        (
            exceptions.PermissionDenied("test detail"),
            "error: failed to cancel execution",
        ),
    ],
)
@mock.patch(EXECUTIONS_CLIENT)
def test_cancel_execution_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected: str,
) -> None:
    mock_client_class.return_value.cancel_execution.side_effect = error

    cancel_execution.cancel_execution(
        PROJECT_ID, LOCATION_ID, WORKFLOW_ID, EXECUTION_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected)
    assert "test detail" in err


@conftest.live_only
def test_cancel_execution_live(
    capsys: pytest.CaptureFixture[str],
    executions_client: executions_v1.ExecutionsClient,
    sleep_workflow_id: str,
) -> None:
    parent = (
        f"projects/{conftest.LIVE_PROJECT_ID}/locations/{conftest.LIVE_LOCATION_ID}"
        f"/workflows/{sleep_workflow_id}"
    )
    execution = executions_client.create_execution(parent=parent)
    execution_id = execution.name.rsplit("/", 1)[-1]

    cancel_execution.cancel_execution(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_LOCATION_ID,
        sleep_workflow_id,
        execution_id,
    )

    assert "State: CANCELLED" in capsys.readouterr().out
