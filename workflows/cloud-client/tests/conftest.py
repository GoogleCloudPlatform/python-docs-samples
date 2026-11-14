# Copyright 2025 Google LLC
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

"""Shared live-test fixtures for Cloud Workflows client-library samples.

Tests marked with `live_only` are skipped unless RUN_INTEGRATION_TESTS is "true".
"""

import os
import pathlib
from typing import Iterator
import uuid

from google.api_core import exceptions
from google.cloud import workflows_v1
from google.cloud.workflows import executions_v1
import pytest

LIVE_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LIVE_LOCATION_ID = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
LIVE_SERVICE_ACCOUNT_EMAIL = os.environ.get("SERVICE_ACCOUNT_EMAIL", "")
MY_FIRST_WORKFLOW = (
    pathlib.Path(__file__).resolve().parent.parent / "myFirstWorkflow.workflows.yaml"
).read_text()
SLEEP_WORKFLOW = """
main:
  steps:
    - wait:
        call: sys.sleep
        args:
          seconds: 300
"""
FAILING_WORKFLOW = """
main:
  steps:
    - fail:
        raise: "example-failure"
"""

live_only = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION_TESTS") != "true",
    reason="Set RUN_INTEGRATION_TESTS=true to run integration tests.",
)


@pytest.fixture(scope="session")
def workflows_client() -> workflows_v1.WorkflowsClient:
    return workflows_v1.WorkflowsClient()


@pytest.fixture(scope="session")
def executions_client() -> executions_v1.ExecutionsClient:
    return executions_v1.ExecutionsClient()


def deploy_workflow(client: workflows_v1.WorkflowsClient, source: str) -> Iterator[str]:
    """Deploys a test workflow with a unique ID and deletes it afterward."""
    workflow_id = f"test-workflow-{uuid.uuid4().hex[:12]}"
    client.create_workflow(
        parent=f"projects/{LIVE_PROJECT_ID}/locations/{LIVE_LOCATION_ID}",
        workflow=workflows_v1.Workflow(
            source_contents=source, service_account=LIVE_SERVICE_ACCOUNT_EMAIL
        ),
        workflow_id=workflow_id,
    ).result(timeout=300)
    yield workflow_id
    try:
        client.delete_workflow(
            name=f"projects/{LIVE_PROJECT_ID}/locations/{LIVE_LOCATION_ID}/workflows/{workflow_id}"
        ).result(timeout=300)
    except exceptions.NotFound:
        pass


@pytest.fixture(scope="session")
def my_first_workflow_id(
    workflows_client: workflows_v1.WorkflowsClient,
) -> Iterator[str]:
    yield from deploy_workflow(workflows_client, MY_FIRST_WORKFLOW)


@pytest.fixture
def sleep_workflow_id(
    workflows_client: workflows_v1.WorkflowsClient,
) -> Iterator[str]:
    yield from deploy_workflow(workflows_client, SLEEP_WORKFLOW)


@pytest.fixture
def failing_workflow_id(
    workflows_client: workflows_v1.WorkflowsClient,
) -> Iterator[str]:
    yield from deploy_workflow(workflows_client, FAILING_WORKFLOW)


@pytest.fixture
def new_workflow_id(
    workflows_client: workflows_v1.WorkflowsClient,
) -> Iterator[str]:
    """Provides an unused workflow ID and deletes the workflow afterward."""
    workflow_id = f"test-workflow-{uuid.uuid4().hex[:12]}"
    yield workflow_id
    try:
        workflows_client.delete_workflow(
            name=f"projects/{LIVE_PROJECT_ID}/locations/{LIVE_LOCATION_ID}/workflows/{workflow_id}"
        ).result(timeout=300)
    except exceptions.NotFound:
        pass
