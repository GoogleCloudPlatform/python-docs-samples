# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file contains code samples that demonstrate how to set policy for project.

# [START iam_query_testable_permissions]
import os
from typing import List

from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2


def query_testable_permissions(
    project_id: str, permissions: List[str]
) -> policy_pb2.Policy:
    """Tests IAM permissions of the caller.

    project_id: ID or number of the Google Cloud project you want to use.
    permissions: List of permissions to get.
    """

    client = resourcemanager_v3.ProjectsClient()
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = f"projects/{project_id}"
    request.permissions.extend(permissions)

    permissions_reponse = client.test_iam_permissions(request)
    print(permissions_reponse)
    return permissions_reponse.permissions
# [END iam_query_testable_permissions]


if __name__ == "__main__":
    # To run the sample you would need
    # resourcemanager.projects.setIamPolicy (roles/resourcemanager.projectIamAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "test-project-id")

    permissions = [
        "resourcemanager.projects.get",
        "resourcemanager.projects.delete",
    ]

    query_testable_permissions(PROJECT_ID, permissions)
