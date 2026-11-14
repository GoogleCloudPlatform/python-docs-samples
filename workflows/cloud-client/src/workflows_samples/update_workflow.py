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

# [START workflows_update_workflow]
import sys

from google.api_core import exceptions
from google.cloud import workflows_v1
from google.protobuf import field_mask_pb2


def update_workflow(project_id: str, location_id: str, workflow_id: str) -> None:
    """Updates a workflow's description and labels.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the workflow (for example, 'us-central1').
        workflow_id: The ID of the workflow (for example, 'example-workflow').
    """
    client = workflows_v1.WorkflowsClient()
    name = f"projects/{project_id}/locations/{location_id}/workflows/{workflow_id}"

    workflow = workflows_v1.Workflow(
        name=name,
        description="example-description",
        labels={"environment": "example-updated"},
    )
    # Only fields in the update mask change.
    update_mask = field_mask_pb2.FieldMask(paths=["description", "labels"])

    try:
        operation = client.update_workflow(workflow=workflow, update_mask=update_mask)
        print("Waiting for the update to finish...")
        response = operation.result(timeout=300)
    except exceptions.NotFound as err:
        print(
            f"error: workflow '{workflow_id}' not found "
            f"in location '{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to update workflow '{workflow_id}' "
            f"in location '{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {response.name}")
        print(f"Description: {response.description}")
        print(f"Labels: {dict(response.labels)}")
        print(f"Revision ID: {response.revision_id}")


# [END workflows_update_workflow]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=update_workflow.__doc__.splitlines()[0]
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

    update_workflow(
        project_id=args.project_id,
        location_id=args.location_id,
        workflow_id=args.workflow_id,
    )
