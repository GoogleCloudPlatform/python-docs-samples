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

# [START iam_get_role]
from google.api_core.exceptions import NotFound
from google.cloud.iam_admin_v1 import GetRoleRequest, IAMClient, Role


def get_role(project_id: str, role_id: str) -> Role:
    client = IAMClient()
    name = f"projects/{project_id}/roles/{role_id}"
    request = GetRoleRequest(name=name)
    try:
        role = client.get_role(request)
        print(f"Retrieved role: {role_id}: {role}")
        return role
    except NotFound as exc:
        raise NotFound(f"Role with id [{role_id}] not found, take some actions") from exc
# [END iam_get_role]


if __name__ == "__main__":
    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    role_id = "custom1_python"
    get_role(PROJECT_ID, role_id)
