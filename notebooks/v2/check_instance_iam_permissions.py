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

# [START notebooks_v2_check_instance_iam_permissions]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2
from google.iam.v1 import iam_policy_pb2


def check_instance_iam_permissions(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-instance",
) -> None:
    """Checks IAM permissions on a Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone where the instance resides.
        instance_id: The ID of the Workbench instance.
    """
    client = notebooks_v2.NotebookServiceClient()
    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    request = iam_policy_pb2.TestIamPermissionsRequest(
        resource=name,
        permissions=["notebooks.instances.get"],
    )

    try:
        response = client.test_iam_permissions(request=request)
        print(f"Resource ID: {name}")
        print(f"Allowed Permissions: {list(response.permissions)}")
    except exceptions.NotFound as err:
        print(
            f"error: Instance '{instance_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_check_instance_iam_permissions]
