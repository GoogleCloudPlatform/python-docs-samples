# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import uuid

from google.cloud import workflows_v1

import pytest


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
WORKFLOW_ID_BASE = "myFirstWorkflow"


def workflow_exists(client: workflows_v1.WorkflowsClient, workflow_id: str) -> bool:
    """Returns True if the workflow exists in this project."""
    try:
        workflow_name = client.workflow_path(
            PROJECT_ID, LOCATION, workflow_id
        )
        client.get_workflow(request={"name": workflow_name})
        return True
    except Exception as e:
        print(f"Workflow doesn't exist: {e}")
        return False


@pytest.fixture(scope="module")
def client() -> str:
    assert PROJECT_ID, "'GOOGLE_CLOUD_PROJECT' environment variable not set."
    workflows_client = workflows_v1.WorkflowsClient()
    return workflows_client


@pytest.fixture(scope="module")
def project_id() -> str:
    return PROJECT_ID


@pytest.fixture(scope="module")
def location() -> str:
    return LOCATION


@pytest.fixture(scope="function")
def workflow_id(client: workflows_v1.WorkflowsClient) -> str:
    workflow_id_str = f"{WORKFLOW_ID_BASE}_{uuid.uuid4()}"

    creating_workflow = False
    backoff_delay = 1  # Start wait with delay of 1 second.

    # Create the workflow if it doesn't exist.
    while not workflow_exists(client, workflow_id_str):
        if not creating_workflow:
            # Create the workflow.
            workflow_file = open("myFirstWorkflow.workflows.yaml").read()

            parent = client.common_location_path(PROJECT_ID, LOCATION)

            client.create_workflow(
                request={
                    "parent": parent,
                    "workflow_id": workflow_id_str,
                    "workflow": {
                        "name": workflow_id_str,
                        "source_contents": workflow_file
                    },
                }
            )

            creating_workflow = True

        # Wait until the workflow is created.
        print("- Waiting for the Workflow to be created...")
        time.sleep(backoff_delay)
        # Double the delay to provide exponential backoff.
        backoff_delay *= 2

    yield workflow_id_str

    # Delete the workflow.
    workflow_full_name = client.workflow_path(
        PROJECT_ID, LOCATION, workflow_id_str
    )

    client.delete_workflow(
        request={
            "name": workflow_full_name,
        }
    )
