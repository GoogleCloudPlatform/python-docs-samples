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
from workflows_samples import create_workflow

from . import conftest

PROJECT_ID = "test-project"
LOCATION_ID = "us-central1"
WORKFLOW_ID = "test-workflow"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
WORKFLOW_NAME = f"{PARENT}/workflows/{WORKFLOW_ID}"
WORKFLOWS_CLIENT = "google.cloud.workflows_v1.WorkflowsClient"


@mock.patch(WORKFLOWS_CLIENT)
def test_create_workflow_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.create_workflow.return_value.result.return_value = workflows_v1.Workflow(
        name=WORKFLOW_NAME,
        revision_id="000002-abc",
        state=workflows_v1.Workflow.State.ACTIVE,
        description="example-description",
        labels={"environment": "example-updated"},
        call_log_level=workflows_v1.Workflow.CallLogLevel.LOG_ERRORS_ONLY,
    )

    create_workflow.create_workflow(
        PROJECT_ID,
        LOCATION_ID,
        WORKFLOW_ID,
        "runner@test-project.iam.gserviceaccount.com",
    )

    kwargs = client.create_workflow.call_args.kwargs
    assert kwargs["parent"] == PARENT
    assert kwargs["workflow_id"] == WORKFLOW_ID
    workflow = kwargs["workflow"]
    assert workflow.service_account == "runner@test-project.iam.gserviceaccount.com"
    assert workflow.call_log_level == workflows_v1.Workflow.CallLogLevel.LOG_ERRORS_ONLY
    assert workflow.user_env_vars["EXAMPLE_GREETING"] == "example-greeting"
    assert "EXAMPLE_GREETING" in workflow.source_contents
    out, err = capsys.readouterr()
    assert "Waiting for the workflow to deploy..." in out
    assert f"Resource ID: {WORKFLOW_NAME}" in out
    assert "Call Log Level: LOG_ERRORS_ONLY" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected",
    [
        (
            exceptions.AlreadyExists("test detail"),
            "error: workflow 'test-workflow' already exists",
        ),
        (
            exceptions.PermissionDenied("test detail"),
            "error: failed to create workflow",
        ),
    ],
)
@mock.patch(WORKFLOWS_CLIENT)
def test_create_workflow_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected: str,
) -> None:
    mock_client_class.return_value.create_workflow.side_effect = error

    create_workflow.create_workflow(
        PROJECT_ID,
        LOCATION_ID,
        WORKFLOW_ID,
        "runner@test-project.iam.gserviceaccount.com",
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected)
    assert "test detail" in err


@conftest.live_only
def test_create_workflow_live(
    capsys: pytest.CaptureFixture[str], new_workflow_id: str
) -> None:
    create_workflow.create_workflow(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_LOCATION_ID,
        new_workflow_id,
        conftest.LIVE_SERVICE_ACCOUNT_EMAIL,
    )

    out, err = capsys.readouterr()
    parent = (
        f"projects/{conftest.LIVE_PROJECT_ID}/locations/{conftest.LIVE_LOCATION_ID}"
        f"/workflows/{new_workflow_id}"
    )
    assert f"Resource ID: {parent}" in out
    assert "Call Log Level: LOG_ERRORS_ONLY" in out
    assert "error:" not in err
