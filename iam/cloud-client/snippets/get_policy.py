# Copyright 2024 Google LLC
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

# This file contains code samples that demonstrate how to get policy for service account.

import os

# [START iam_get_policy]
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2


def get_project_policy(project_id: str) -> policy_pb2.Policy:
    """Get policy for project.

    project_id: ID or number of the Google Cloud project you want to use.
    """

    client = resourcemanager_v3.ProjectsClient()
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = f"projects/{project_id}"

    policy = client.get_iam_policy(request)
    print(f"Policy retrieved: {policy}")

    return policy
# [END iam_get_policy]


if __name__ == "__main__":
    # To run the sample you would need
    # resourcemanager.projects.getIamPolicy (roles/resourcemanager.projectIamAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    policy = get_project_policy(PROJECT_ID)
