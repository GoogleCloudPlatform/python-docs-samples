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

# [START iam_list_roles]
from google.cloud.iam_admin_v1 import IAMClient, ListRolesRequest, RoleView
from google.cloud.iam_admin_v1.services.iam.pagers import ListRolesPager


def list_roles(
    project_id: str, show_deleted: bool = True, role_view: RoleView = RoleView.BASIC
) -> ListRolesPager:
    """Lists IAM roles in a GCP project.

    Args:
        project_id: GCP project ID
        show_deleted: Whether to include deleted roles in the results
        role_view: Level of detail for the returned roles (e.g., BASIC or FULL)

    Returns: A pager for traversing through the roles
    """

    client = IAMClient()
    parent = f"projects/{project_id}"
    request = ListRolesRequest(parent=parent, show_deleted=show_deleted, view=role_view)
    roles = client.list_roles(request)
    for page in roles.pages:
        for role in page.roles:
            print(role)
    print("Listed all iam roles")
    return roles
# [END iam_list_roles]


if __name__ == "__main__":
    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    list_roles(PROJECT_ID)
