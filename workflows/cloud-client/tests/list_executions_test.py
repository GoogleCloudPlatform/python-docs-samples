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

import time
from unittest import mock

from google.api_core import exceptions
from google.cloud.workflows import executions_v1
import pytest
from workflows_samples import list_executions

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
def test_list_executions_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.list_executions.return_value = [
        executions_v1.Execution(
            name=EXECUTION_NAME,
            state=executions_v1.Execution.State.FAILED,
            error=executions_v1.Execution.Error(payload="boom"),
        )
    ]

    list_executions.list_executions(PROJECT_ID, LOCATION_ID, WORKFLOW_ID)

    request = client.list_executions.call_args.kwargs["request"]
    assert request.parent == WORKFLOW_NAME
    assert request.filter == 'state="FAILED"'
    assert request.order_by == "createTime desc"
    assert request.view == executions_v1.ExecutionView.FULL
    out, err = capsys.readouterr()
    assert f"Resource ID: {EXECUTION_NAME}" in out
    assert "Error: boom" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected",
    [
        (
            exceptions.NotFound("test detail"),
            "error: workflow 'test-workflow' not found",
        ),
        (
            exceptions.PermissionDenied("test detail"),
            "error: failed to list executions",
        ),
    ],
)
@mock.patch(EXECUTIONS_CLIENT)
def test_list_executions_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected: str,
) -> None:
    mock_client_class.return_value.list_executions.side_effect = error

    list_executions.list_executions(PROJECT_ID, LOCATION_ID, WORKFLOW_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected)
    assert "test detail" in err


@conftest.live_only
def test_list_failed_executions_live(
    capsys: pytest.CaptureFixture[str],
    executions_client: executions_v1.ExecutionsClient,
    failing_workflow_id: str,
) -> None:
    parent = (
        f"projects/{conftest.LIVE_PROJECT_ID}/locations/{conftest.LIVE_LOCATION_ID}"
        f"/workflows/{failing_workflow_id}"
    )
    execution = executions_client.create_execution(parent=parent)
    deadline = time.monotonic() + 120
    while execution.state == executions_v1.Execution.State.ACTIVE:
        assert time.monotonic() < deadline, "The execution didn't finish."
        time.sleep(2)
        execution = executions_client.get_execution(name=execution.name)

    list_executions.list_executions(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_LOCATION_ID, failing_workflow_id
    )

    out = capsys.readouterr().out
    assert f"Resource ID: {execution.name}" in out
    assert "example-failure" in out
