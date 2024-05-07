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

# [START iam_modify_policy_remove_member]
from google.iam.v1 import policy_pb2
from snippets.get_policy import get_project_policy
from snippets.set_policy import set_project_policy


def modify_policy_remove_member(
    project_id: str, role: str, member: str
) -> policy_pb2.Policy:
    """
    Remove a member from certain role in project policy.

    project_id: ID or number of the Google Cloud project you want to use.
    role: role to which member need to be added.
    member: The principals requesting access.

    Possible format for member:
        * user:{emailid}
        * serviceAccount:{emailid}
        * group:{emailid}
        * deleted:user:{emailid}?uid={uniqueid}
        * deleted:serviceAccount:{emailid}?uid={uniqueid}
        * deleted:group:{emailid}?uid={uniqueid}
        * domain:{domain}
    """
    policy = get_project_policy(project_id)

    for bind in policy.bindings:
        if bind.role == role:
            if member in bind.members:
                bind.members.remove(member)
            break

    return set_project_policy(project_id, policy, False)


# [END iam_modify_policy_remove_member]


if __name__ == "__main__":
    # To run the sample you would need
    # resourcemanager.projects.setIamPolicy (roles/resourcemanager.projectIamAdmin)

    # Your Google Cloud project ID.
    project_id = "test-project-id"
    role = "roles/viewer"
    member = f"serviceAccount:test-service-account@{project_id}.iam.gserviceaccount.com"

    modify_policy_remove_member(project_id, role, member)
