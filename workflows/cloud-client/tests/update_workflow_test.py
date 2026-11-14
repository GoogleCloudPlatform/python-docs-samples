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
from workflows_samples import update_workflow

from . import conftest

PROJECT_ID = "test-project"
LOCATION_ID = "us-central1"
WORKFLOW_ID = "test-workflow"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
WORKFLOW_NAME = f"{PARENT}/workflows/{WORKFLOW_ID}"
WORKFLOWS_CLIENT = "google.cloud.workflows_v1.WorkflowsClient"


@mock.patch(WORKFLOWS_CLIENT)
def test_update_workflow_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.update_workflow.return_value.result.return_value = workflows_v1.Workflow(
        name=WORKFLOW_NAME,
        revision_id="000002-abc",
        state=workflows_v1.Workflow.State.ACTIVE,
        description="example-description",
        labels={"environment": "example-updated"},
        call_log_level=workflows_v1.Workflow.CallLogLevel.LOG_ERRORS_ONLY,
    )

    update_workflow.update_workflow(PROJECT_ID, LOCATION_ID, WORKFLOW_ID)

    kwargs = client.update_workflow.call_args.kwargs
    assert kwargs["workflow"].name == WORKFLOW_NAME
    assert list(kwargs["update_mask"].paths) == ["description", "labels"]
    out, err = capsys.readouterr()
    assert "Description: example-description" in out
    assert "Labels: {'environment': 'example-updated'}" in out
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
            "error: failed to update workflow",
        ),
    ],
)
@mock.patch(WORKFLOWS_CLIENT)
def test_update_workflow_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected: str,
) -> None:
    mock_client_class.return_value.update_workflow.side_effect = error

    update_workflow.update_workflow(PROJECT_ID, LOCATION_ID, WORKFLOW_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected)
    assert "test detail" in err


@conftest.live_only
def test_update_workflow_live(
    capsys: pytest.CaptureFixture[str],
    workflows_client: workflows_v1.WorkflowsClient,
    new_workflow_id: str,
) -> None:
    workflows_client.create_workflow(
        parent=f"projects/{conftest.LIVE_PROJECT_ID}/locations/{conftest.LIVE_LOCATION_ID}",
        workflow=workflows_v1.Workflow(
            source_contents=conftest.MY_FIRST_WORKFLOW,
            service_account=conftest.LIVE_SERVICE_ACCOUNT_EMAIL,
        ),
        workflow_id=new_workflow_id,
    ).result(timeout=300)

    update_workflow.update_workflow(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_LOCATION_ID, new_workflow_id
    )

    out, err = capsys.readouterr()
    assert "Description: example-description" in out
    assert "error:" not in err
