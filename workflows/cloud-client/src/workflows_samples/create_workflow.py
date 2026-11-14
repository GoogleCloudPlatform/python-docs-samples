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

# [START workflows_create_workflow]
import sys

from google.api_core import exceptions
from google.cloud import workflows_v1


def create_workflow(
    project_id: str, location_id: str, workflow_id: str, service_account_email: str
) -> None:
    """Creates a workflow with logging, labels, and environment variables.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the workflow (for example, 'us-central1').
        workflow_id: The ID for the new workflow (for example, 'example-workflow').
        service_account_email: The service account that the workflow runs as.
    """
    client = workflows_v1.WorkflowsClient()
    parent = f"projects/{project_id}/locations/{location_id}"

    # The workflow definition, in YAML. It returns a greeting from an
    # environment variable that's set on the workflow below.
    source_contents = """
main:
  steps:
    - greet:
        return: ${sys.get_env("EXAMPLE_GREETING")}
"""
    workflow = workflows_v1.Workflow(
        source_contents=source_contents,
        service_account=service_account_email,
        # Logs each call that fails, without logging successful calls.
        call_log_level=workflows_v1.Workflow.CallLogLevel.LOG_ERRORS_ONLY,
        labels={"environment": "example"},
        user_env_vars={"EXAMPLE_GREETING": "example-greeting"},
    )

    try:
        operation = client.create_workflow(
            parent=parent, workflow=workflow, workflow_id=workflow_id
        )
        print("Waiting for the workflow to deploy...")
        response = operation.result(timeout=300)
    except exceptions.AlreadyExists as err:
        print(
            f"error: workflow '{workflow_id}' already exists "
            f"in location '{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create workflow '{workflow_id}' "
            f"in location '{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {response.name}")
        print(f"Creation Date: {response.create_time}")
        print(f"Call Log Level: {response.call_log_level.name}")
        print(f"Revision ID: {response.revision_id}")
        print(f"State: {response.state.name}")


# [END workflows_create_workflow]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=create_workflow.__doc__.splitlines()[0]
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
        default=os.environ.get("WORKFLOW_ID", "example-workflow"),
        help="ID for the new workflow (default: $WORKFLOW_ID)",
    )
    parser.add_argument(
        "--service-account-email",
        default=os.environ.get("SERVICE_ACCOUNT_EMAIL"),
        help="Service account the workflow runs as (default: $SERVICE_ACCOUNT_EMAIL)",
    )
    args = parser.parse_args()
    service_account_email = (
        args.service_account_email
        or f"example-runner@{args.project_id}.iam.gserviceaccount.com"
    )

    create_workflow(
        project_id=args.project_id,
        location_id=args.location_id,
        workflow_id=args.workflow_id,
        service_account_email=service_account_email,
    )
