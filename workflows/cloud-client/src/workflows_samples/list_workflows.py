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

# [START workflows_client_library]
import sys

from google.api_core import exceptions
from google.cloud import workflows_v1


def list_workflows(project_id: str, location_id: str) -> None:
    """Lists the workflows in a location.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the workflow (for example, 'us-central1').
    """
    client = workflows_v1.WorkflowsClient()
    parent = f"projects/{project_id}/locations/{location_id}"

    try:
        # The client fetches more pages as the loop needs them.
        for workflow in client.list_workflows(parent=parent):
            print(f"Resource ID: {workflow.name}")
            print(f"Creation Date: {workflow.create_time}")
            print(f"Revision ID: {workflow.revision_id}")
            print(f"State: {workflow.state.name}")
    except exceptions.InvalidArgument as err:
        print(
            f"error: invalid location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to list workflows "
            f"in location '{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END workflows_client_library]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(description=list_workflows.__doc__.splitlines()[0])
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
    args = parser.parse_args()

    list_workflows(
        project_id=args.project_id,
        location_id=args.location_id,
    )
