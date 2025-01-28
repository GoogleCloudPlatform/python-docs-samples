# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os


# [START iam_disable_role]
from google.api_core.exceptions import NotFound
from google.cloud.iam_admin_v1 import GetRoleRequest, IAMClient, Role, UpdateRoleRequest


def disable_role(project_id: str, role_id: str) -> Role:
    """Disables an IAM role in a GCP project.

    Args:
        project_id: GCP project ID
        role_id: ID of GCP IAM role

    Returns: Updated google.cloud.iam_admin_v1.Role object with disabled stage
    """
    client = IAMClient()
    name = f"projects/{project_id}/roles/{role_id}"
    get_request = GetRoleRequest(name=name)
    try:
        role = client.get_role(get_request)
        role.stage = Role.RoleLaunchStage.DISABLED
        update_request = UpdateRoleRequest(name=role.name, role=role)
        client.update_role(update_request)
        print(f"Disabled role: {role_id}: {role}")
        return role
    except NotFound as exc:
        raise NotFound(f'Role with id [{role_id}] not found, take some actions') from exc
# [END iam_disable_role]


if __name__ == "__main__":
    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    role_id = "custom1_python"
    disable_role(PROJECT_ID, role_id)
