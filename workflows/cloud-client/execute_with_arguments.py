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

# Deprecated: moved to src/workflows_samples/execute_with_arguments.py. Kept until docs pages
# embed the new path.
# [START workflows_execute_with_arguments]
import json
import sys
import time

from google.api_core import exceptions
from google.cloud.workflows import executions_v1


def execute_workflow_with_arguments(
    project_id: str, location_id: str, workflow_id: str
) -> None:
    """Runs a workflow with input arguments and waits for it to finish.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the workflow (for example, 'us-central1').
        workflow_id: The ID of the workflow to run (for example, 'myFirstWorkflow').
    """
    client = executions_v1.ExecutionsClient()
    parent = f"projects/{project_id}/locations/{location_id}/workflows/{workflow_id}"

    # The workflow receives the argument as its runtime input (params: [args]).
    argument = json.dumps({"searchTerm": "Cloud"})
    execution = executions_v1.Execution(argument=argument)

    try:
        execution = client.create_execution(parent=parent, execution=execution)
        print(f"Waiting for execution {execution.name} to finish...")
        # Executions run asynchronously. Poll with exponential backoff until done.
        delay_seconds = 1
        while execution.state == executions_v1.Execution.State.ACTIVE:
            time.sleep(delay_seconds)
            delay_seconds = min(delay_seconds * 2, 30)
            execution = client.get_execution(name=execution.name)
    except exceptions.NotFound as err:
        print(
            f"error: workflow '{workflow_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to run workflow '{workflow_id}' in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {execution.name}")
        if execution.state == executions_v1.Execution.State.FAILED:
            print(f"Error: {execution.error.payload}")
        print(f"Result: {execution.result}")
        print(f"State: {execution.state.name}")


# [END workflows_execute_with_arguments]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=execute_workflow_with_arguments.__doc__.splitlines()[0]
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--location-id",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="Region of the workflow (default: $GOOGLE_CLOUD_LOCATION)",
    )
    parser.add_argument(
        "--workflow-id",
        default=os.environ.get("WORKFLOW_ID", "myFirstWorkflow"),
        help="ID of the workflow (default: $WORKFLOW_ID)",
    )
    args = parser.parse_args()

    execute_workflow_with_arguments(
        project_id=args.project_id,
        location_id=args.location_id,
        workflow_id=args.workflow_id,
    )
