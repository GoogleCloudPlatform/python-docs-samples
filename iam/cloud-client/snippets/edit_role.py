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

# [START iam_edit_role]
from google.api_core.exceptions import NotFound
from google.cloud.iam_admin_v1 import IAMClient, Role, UpdateRoleRequest

from snippets.get_role import get_role


def edit_role(role: Role) -> Role:
    """Edits an existing IAM role in a GCP project.

    Args:
        role: google.cloud.iam_admin_v1.Role object to be updated

    Returns: Updated google.cloud.iam_admin_v1.Role object
    """
    client = IAMClient()
    request = UpdateRoleRequest(name=role.name, role=role)
    try:
        role = client.update_role(request)
        print(f"Edited role: {role.name}: {role}")
        return role
    except NotFound:
        print(f"Role [{role.name}] not found, take some actions")
# [END iam_edit_role]


if __name__ == "__main__":
    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    role_id = "custom1_python_duplicate5"
    role = get_role(PROJECT_ID, role_id + "sadf")

    role.title = "Update_python_title2"
    upd_role = edit_role(role)
