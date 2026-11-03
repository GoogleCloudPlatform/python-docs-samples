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

# [START notebooks_v2_get_instance_iam_policy]
from google.api_core import exceptions
from google.cloud import notebooks_v2
from google.iam.v1 import iam_policy_pb2


def get_instance_iam_policy(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-instance",
) -> None:
    """Gets the IAM policy for a Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone where the instance resides.
        instance_id: The ID of the Workbench instance.
    """
    client = notebooks_v2.NotebookServiceClient()
    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    request = iam_policy_pb2.GetIamPolicyRequest(resource=name)

    try:
        response = client.get_iam_policy(request=request)
        print(f"Resource ID: {name}")
        print(f"Policy Etag: {response.etag}")
        print(f"Policy Version: {response.version}")
        for binding in response.bindings:
            print(f"Role: {binding.role}")
    except exceptions.NotFound as err:
        print(
            f"error: Instance '{instance_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_get_instance_iam_policy]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get the IAM policy for a Workbench instance."
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
    get_instance_iam_policy(
        project_id=args.project_id,
        location_id=args.location_id,
        instance_id=args.instance_id,
    )
