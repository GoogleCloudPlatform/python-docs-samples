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

# [START workflows_cancel_execution]
import sys

from google.api_core import exceptions
from google.cloud.workflows import executions_v1


def cancel_execution(
    project_id: str, location_id: str, workflow_id: str, execution_id: str
) -> None:
    """Cancels an execution that's still running.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the workflow (for example, 'us-central1').
        workflow_id: The ID of the workflow (for example, 'myFirstWorkflow').
        execution_id: The ID of the execution.
    """
    client = executions_v1.ExecutionsClient()
    name = (
        f"projects/{project_id}/locations/{location_id}/workflows/{workflow_id}"
        f"/executions/{execution_id}"
    )

    try:
        execution = client.cancel_execution(name=name)
    except exceptions.NotFound as err:
        print(
            f"error: execution '{execution_id}' not found "
            f"for workflow '{workflow_id}' in location '{location_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to cancel execution '{execution_id}' "
            f"for workflow '{workflow_id}' in location '{location_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {execution.name}")
        print(f"End Time: {execution.end_time}")
        print(f"State: {execution.state.name}")


# [END workflows_cancel_execution]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=cancel_execution.__doc__.splitlines()[0]
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
    parser.add_argument(
        "--execution-id",
        default=os.environ.get("EXECUTION_ID", "example-execution-id"),
        help="ID of the execution (default: $EXECUTION_ID)",
    )
    args = parser.parse_args()

    cancel_execution(
        project_id=args.project_id,
        location_id=args.location_id,
        workflow_id=args.workflow_id,
        execution_id=args.execution_id,
    )
