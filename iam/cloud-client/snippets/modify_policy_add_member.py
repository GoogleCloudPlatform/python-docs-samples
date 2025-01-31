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

import os

# [START iam_modify_policy_add_member]
from google.iam.v1 import policy_pb2
from snippets.get_policy import get_project_policy
from snippets.set_policy import set_project_policy


def modify_policy_add_principal(
    project_id: str, role: str, principal: str
) -> policy_pb2.Policy:
    """Add a principal to certain role in project policy.

    project_id: ID or number of the Google Cloud project you want to use.
    role: role to which principal need to be added.
    principal: The principal requesting access.

    For principal ID formats, see https://cloud.google.com/iam/docs/principal-identifiers
    """
    policy = get_project_policy(project_id)

    for bind in policy.bindings:
        if bind.role == role:
            bind.members.append(principal)
            break

    return set_project_policy(project_id, policy)
# [END iam_modify_policy_add_member]


if __name__ == "__main__":
    # To run the sample you would need
    # resourcemanager.projects.setIamPolicy (roles/resourcemanager.projectIamAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    role = "roles/viewer"
    principal = f"serviceAccount:test-service-account@{PROJECT_ID}.iam.gserviceaccount.com"

    modify_policy_add_principal(PROJECT_ID, role, principal)
