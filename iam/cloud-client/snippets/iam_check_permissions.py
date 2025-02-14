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

from typing import List

from google.cloud import resourcemanager_v3


# [START iam_test_permissions]
def test_permissions(project_id: str) -> List[str]:
    """Tests IAM permissions of currently authenticated user to a project."""

    projects_client = resourcemanager_v3.ProjectsClient()
    if not project_id.startswith("projects/"):
        project_id = "projects/" + project_id

    owned_permissions = projects_client.test_iam_permissions(
        resource=project_id,
        permissions=["resourcemanager.projects.get", "resourcemanager.projects.delete"],
    ).permissions

    print("Currently authenticated user has following permissions:", owned_permissions)
    return owned_permissions
# [END iam_test_permissions]
