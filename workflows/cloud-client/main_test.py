# Copyright 2021 Google LLC
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

from google.cloud import workflows_v1
from google.cloud.workflows.executions_v1.types import executions
import main

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
WORKFLOW_ID = "myFirstWorkflow"


def test_workflow_execution():
    assert PROJECT != ""

    if not workflow_exists():
        workflow_file = open("myFirstWorkflow.workflows.yaml", "r").read()

        workflows_client = workflows_v1.WorkflowsClient()
        workflows_client.create_workflow(request={
            # Manually construct the location
            # https://github.com/googleapis/python-workflows/issues/21
            "parent": f'projects/{PROJECT}/locations/{LOCATION}',
            "workflow_id": WORKFLOW_ID,
            "workflow": {
                "name": WORKFLOW_ID,
                "source_contents": workflow_file
            }
        })

    result = main.execute_workflow(PROJECT)
    assert result.state == executions.Execution.State.SUCCESS
    assert len(result.result) > 0


def workflow_exists():
    """Returns True if the workflow exists in this project
    """
    try:
        workflows_client = workflows_v1.WorkflowsClient()
        workflow_name = workflows_client.workflow_path(PROJECT, LOCATION, WORKFLOW_ID)
        workflows_client.get_workflow(request={"name": workflow_name})
        return True
    except Exception as e:
        print(f"Workflow doesn't exist: {e}")
        return False
