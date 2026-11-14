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

# [START workflows_list_executions]
import sys

from google.api_core import exceptions
from google.cloud.workflows import executions_v1


def list_executions(project_id: str, location_id: str, workflow_id: str) -> None:
    """Lists a workflow's failed executions, newest first.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the workflow (for example, 'us-central1').
        workflow_id: The ID of the workflow (for example, 'myFirstWorkflow').
    """
    client = executions_v1.ExecutionsClient()
    parent = f"projects/{project_id}/locations/{location_id}/workflows/{workflow_id}"
    request = executions_v1.ListExecutionsRequest(
        parent=parent,
        filter='state="FAILED"',
        order_by="createTime desc",
        # The default BASIC view leaves out each execution's error and result.
        view=executions_v1.ExecutionView.FULL,
    )

    try:
        # The client fetches more pages as the loop needs them.
        for execution in client.list_executions(request=request):
            error_payload = execution.error.payload if execution.error else ""
            print(f"Resource ID: {execution.name}")
            print(f"Error: {error_payload}")
            print(f"Start Time: {execution.start_time}")
    except exceptions.NotFound as err:
        print(
            f"error: workflow '{workflow_id}' not found "
            f"in location '{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list executions "
            f"for workflow '{workflow_id}' in location '{location_id}': {err.message}",
            file=sys.stderr,
        )


# [END workflows_list_executions]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=list_executions.__doc__.splitlines()[0]
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

    list_executions(
        project_id=args.project_id,
        location_id=args.location_id,
        workflow_id=args.workflow_id,
    )
