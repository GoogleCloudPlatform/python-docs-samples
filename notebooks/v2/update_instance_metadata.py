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

# [START notebooks_v2_update_instance_metadata]
from google.api_core import exceptions
from google.cloud import notebooks_v2
from google.protobuf import field_mask_pb2


def update_instance_metadata(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-instance",
) -> None:
    """Updates custom metadata on a Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone where the instance resides.
        instance_id: The ID of the Workbench instance to update.
    """
    client = notebooks_v2.NotebookServiceClient()
    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    gce_setup = notebooks_v2.GceSetup(
        metadata={"idle-timeout-seconds": "3600"},
    )
    instance = notebooks_v2.Instance(name=name, gce_setup=gce_setup)
    update_mask = field_mask_pb2.FieldMask(paths=["gce_setup.metadata"])
    request = notebooks_v2.UpdateInstanceRequest(
        instance=instance,
        update_mask=update_mask,
    )

    try:
        operation = client.update_instance(request=request)
        print(f"Waiting for operation to complete: {operation.operation.name}")
        response = operation.result()
        print(f"Resource ID: {response.name}")
        print(f"Metadata: {response.gce_setup.metadata}")
        print(f"State: {response.state.name}")
    except exceptions.NotFound as err:
        print(
            f"error: Instance '{instance_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_update_instance_metadata]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update custom metadata on a Workbench instance."
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
    args = parser.parse_args()
    update_instance_metadata(
        project_id=args.project_id,
        location_id=args.location_id,
        instance_id=args.instance_id,
    )
