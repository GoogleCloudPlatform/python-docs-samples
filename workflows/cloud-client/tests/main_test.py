# Copyright 2021 Google LLC
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
from workflows_samples import main

from . import conftest

PROJECT_ID = "test-project"
LOCATION_ID = "us-central1"
WORKFLOW_ID = "test-workflow"
EXECUTION_ID = "test-execution"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
WORKFLOW_NAME = f"{PARENT}/workflows/{WORKFLOW_ID}"
EXECUTION_NAME = f"{WORKFLOW_NAME}/executions/{EXECUTION_ID}"
EXECUTIONS_CLIENT = "google.cloud.workflows.executions_v1.ExecutionsClient"


@mock.patch.object(main.time, "sleep")
@mock.patch(EXECUTIONS_CLIENT)
def test_execute_workflow_waits_for_result(
    mock_client_class: mock.MagicMock,
    mock_sleep: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.create_execution.return_value = executions_v1.Execution(
        name=EXECUTION_NAME, state=executions_v1.Execution.State.ACTIVE
    )
    client.get_execution.side_effect = [
        executions_v1.Execution(
            name=EXECUTION_NAME, state=executions_v1.Execution.State.ACTIVE
        ),
        executions_v1.Execution(
            name=EXECUTION_NAME,
            state=executions_v1.Execution.State.SUCCEEDED,
            result='"test result"',
        ),
    ]

    main.execute_workflow(PROJECT_ID, LOCATION_ID, WORKFLOW_ID)

    assert client.create_execution.call_args.kwargs["parent"] == WORKFLOW_NAME

    assert mock_sleep.call_count == 2
    out, err = capsys.readouterr()
    assert f"Resource ID: {EXECUTION_NAME}" in out
    assert 'Result: "test result"' in out
    assert "State: SUCCEEDED" in out
    assert err == ""


@mock.patch.object(main.time, "sleep")
@mock.patch(EXECUTIONS_CLIENT)
def test_execute_workflow_prints_error_when_execution_fails(
    mock_client_class: mock.MagicMock,
    mock_sleep: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.create_execution.return_value = executions_v1.Execution(
        name=EXECUTION_NAME,
        state=executions_v1.Execution.State.FAILED,
        error=executions_v1.Execution.Error(payload="test failure"),
    )

    main.execute_workflow(PROJECT_ID, LOCATION_ID, WORKFLOW_ID)

    out, _ = capsys.readouterr()
    assert "Error: test failure" in out
    assert "State: FAILED" in out


@pytest.mark.parametrize(
    "error, expected",
    [
        (
            exceptions.NotFound("test detail"),
            "error: workflow 'test-workflow' not found",
        ),
        (exceptions.PermissionDenied("test detail"), "error: failed to run workflow"),
    ],
)
@mock.patch(EXECUTIONS_CLIENT)
def test_execute_workflow_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected: str,
) -> None:
    mock_client_class.return_value.create_execution.side_effect = error

    main.execute_workflow(PROJECT_ID, LOCATION_ID, WORKFLOW_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected)
    assert "test detail" in err


@conftest.live_only
def test_execute_workflow_live(
    capsys: pytest.CaptureFixture[str], my_first_workflow_id: str
) -> None:
    main.execute_workflow(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_LOCATION_ID, my_first_workflow_id
    )

    out, err = capsys.readouterr()
    assert "State: SUCCEEDED" in out
    assert "error:" not in err
