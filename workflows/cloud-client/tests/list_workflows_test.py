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
from google.cloud import workflows_v1
import pytest
from workflows_samples import list_workflows

from . import conftest

PROJECT_ID = "test-project"
LOCATION_ID = "us-central1"
WORKFLOW_ID = "test-workflow"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
WORKFLOW_NAME = f"{PARENT}/workflows/{WORKFLOW_ID}"
WORKFLOWS_CLIENT = "google.cloud.workflows_v1.WorkflowsClient"


@mock.patch(WORKFLOWS_CLIENT)
def test_list_workflows_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.list_workflows.return_value = [
        workflows_v1.Workflow(
            name=WORKFLOW_NAME,
            revision_id="000002-abc",
            state=workflows_v1.Workflow.State.ACTIVE,
            description="example-description",
            labels={"environment": "example-updated"},
            call_log_level=workflows_v1.Workflow.CallLogLevel.LOG_ERRORS_ONLY,
        )
    ]

    list_workflows.list_workflows(PROJECT_ID, LOCATION_ID)

    assert client.list_workflows.call_args.kwargs["parent"] == PARENT
    out, err = capsys.readouterr()
    assert f"Resource ID: {WORKFLOW_NAME}" in out
    assert "Revision ID: 000002-abc" in out
    assert "State: ACTIVE" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected",
    [
        (
            exceptions.InvalidArgument("test detail"),
            "error: invalid location 'us-central1'",
        ),
        (exceptions.PermissionDenied("test detail"), "error: failed to list workflows"),
    ],
)
@mock.patch(WORKFLOWS_CLIENT)
def test_list_workflows_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected: str,
) -> None:
    mock_client_class.return_value.list_workflows.side_effect = error

    list_workflows.list_workflows(PROJECT_ID, LOCATION_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected)
    assert "test detail" in err


@conftest.live_only
def test_list_workflows_live(
    capsys: pytest.CaptureFixture[str], my_first_workflow_id: str
) -> None:
    list_workflows.list_workflows(conftest.LIVE_PROJECT_ID, conftest.LIVE_LOCATION_ID)

    out, err = capsys.readouterr()
    assert f"/workflows/{my_first_workflow_id}" in out
    assert "error:" not in err
