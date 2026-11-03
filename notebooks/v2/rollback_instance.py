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

import argparse
import sys

# [START notebooks_v2_rollback_instance]
from google.api_core import exceptions
from google.cloud import notebooks_v2


def rollback_instance(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-instance",
    snapshot_id: str = "example-snapshot",
    revision_id: str = "1",
) -> None:
    """Rolls back a Workbench instance to a snapshot.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone where the instance resides.
        instance_id: The ID of the Workbench instance to roll back.
        snapshot_id: The ID of the Compute Engine snapshot in the project.
        revision_id: The revision ID to roll back to.
    """
    client = notebooks_v2.NotebookServiceClient()
    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    target_snapshot = f"projects/{project_id}/global/snapshots/{snapshot_id}"
    request = notebooks_v2.RollbackInstanceRequest(
        name=name,
        target_snapshot=target_snapshot,
        revision_id=revision_id,
    )

    try:
        operation = client.rollback_instance(request=request)
        print(f"Waiting for operation to complete: {operation.operation.name}")
        response = operation.result()
        print(f"Resource ID: {response.name}")
        print(f"State: {response.state.name}")
    except exceptions.NotFound as err:
        print(
            f"error: Instance '{instance_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_rollback_instance]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Roll back a Workbench instance to a snapshot."
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="The Google Cloud project ID.",
    )
    parser.add_argument(
        "--location-id",
        default="us-central1-a",
        help="The Compute Engine zone.",
    )
    parser.add_argument(
        "--instance-id",
        default="example-instance",
        help="The ID of the Workbench instance.",
    )
    parser.add_argument(
        "--snapshot-id",
        default="example-snapshot",
        help="The ID of the target Compute Engine snapshot.",
    )
    parser.add_argument(
        "--revision-id",
        default="1",
        help="The revision ID for rollback.",
    )
    args = parser.parse_args()
    rollback_instance(
        project_id=args.project_id,
        location_id=args.location_id,
        instance_id=args.instance_id,
        snapshot_id=args.snapshot_id,
        revision_id=args.revision_id,
    )
