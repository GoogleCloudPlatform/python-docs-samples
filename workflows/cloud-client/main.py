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

# [START workflows_api_quickstart]
import time

from google.cloud import workflows_v1
from google.cloud.workflows import executions_v1
from google.cloud.workflows.executions_v1 import Execution
from google.cloud.workflows.executions_v1.types import executions


def execute_workflow(
    project: str, location: str = "us-central1", workflow: str = "myFirstWorkflow"
) -> Execution:
    """Execute a workflow and print the execution results.

    A workflow consists of a series of steps described using the Workflows syntax, and can be written in either YAML or JSON.

    Args:
        project: The Google Cloud project id which contains the workflow to execute.
        location: The location for the workflow
        workflow: The ID of the workflow to execute.

    Returns:
        The execution response.
    """

    # Set up API clients.
    execution_client = executions_v1.ExecutionsClient()
    workflows_client = workflows_v1.WorkflowsClient()

    # Construct the fully qualified location path.
    parent = workflows_client.workflow_path(project, location, workflow)

    # Execute the workflow.
    response = execution_client.create_execution(request={"parent": parent})
    print(f"Created execution: {response.name}")

    # Wait for execution to finish, then print results.
    execution_finished = False
    backoff_delay = 1  # Start wait with delay of 1 second
    print("Poll every second for result...")
    while not execution_finished:
        execution = execution_client.get_execution(request={"name": response.name})
        execution_finished = execution.state != executions.Execution.State.ACTIVE

        # If we haven't seen the result yet, wait a second.
        if not execution_finished:
            print("- Waiting for results...")
            time.sleep(backoff_delay)
            # Double the delay to provide exponential backoff.
            backoff_delay *= 2
        else:
            print(f"Execution finished with state: {execution.state.name}")
            print(f"Execution results: {execution.result}")
            return execution


# [END workflows_api_quickstart]
