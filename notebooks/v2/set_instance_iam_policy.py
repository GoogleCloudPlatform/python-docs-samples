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

# [START notebooks_v2_set_instance_iam_policy]
from google.api_core import exceptions
from google.cloud import notebooks_v2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2


def set_instance_iam_policy(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-instance",
    member: str = "user:example-user@example.com",
    role: str = "roles/notebooks.runner",
) -> None:
    """Sets the IAM policy for a Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone where the instance resides.
        instance_id: The ID of the Workbench instance.
        member: The principal to grant the role to.
        role: The IAM role to bind on the instance.
    """
    client = notebooks_v2.NotebookServiceClient()
    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    binding = policy_pb2.Binding(
        role=role,
        members=[member],
    )
    policy = policy_pb2.Policy(bindings=[binding])
    request = iam_policy_pb2.SetIamPolicyRequest(
        resource=name,
        policy=policy,
    )

    try:
        response = client.set_iam_policy(request=request)
        print(f"Resource ID: {name}")
        print(f"Policy Etag: {response.etag}")
        print(f"Policy Version: {response.version}")
        for item in response.bindings:
            print(f"Role: {item.role}")
    except exceptions.NotFound as err:
        print(
            f"error: Instance '{instance_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_set_instance_iam_policy]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Set the IAM policy for a Workbench instance."
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
        "--member",
        default="user:example-user@example.com",
        help="The IAM principal to grant access to.",
    )
    parser.add_argument(
        "--role",
        default="roles/notebooks.runner",
        help="The IAM role to grant.",
    )
    args = parser.parse_args()
    set_instance_iam_policy(
        project_id=args.project_id,
        location_id=args.location_id,
        instance_id=args.instance_id,
        member=args.member,
        role=args.role,
    )
