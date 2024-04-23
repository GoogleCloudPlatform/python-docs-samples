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

# This file contains code samples that demonstrate how modify policy for project.

# [START iam_modify_policy_add_member]
from typing import Dict, List, Union

from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2


def modify_policy_add_member(
    project_id: str, bindings: List[Dict[str, Union[str, List[str]]]], role: str, member: str
) -> policy_pb2.Policy:
    """
    Add user to existing policy binding.

    project_id: ID or number of the Google Cloud project you want to use.
    bindings: Policy attached to the project, which have to be modified.
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

    client = resourcemanager_v3.ProjectsClient()
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = f"projects/{project_id}"

    set_bindings = []
    for bind in bindings:
        binding = policy_pb2.Binding()
        binding.role = bind["role"]

        if bind["role"] == role:
            bind["members"].append(member)

        binding.members.extend(bind["members"])
        set_bindings.append(binding)

    request.policy.bindings.extend(set_bindings)
    policy = client.set_iam_policy(request)
    return policy

# [END iam_modify_policy_add_member]


if __name__ == "__main__":
    # To run the sample you would need
    # resourcemanager.projects.setIamPolicy (roles/resourcemanager.projectIamAdmin)

    # Your Google Cloud project ID.
    project_id = "test-project-id"
    bindings = [
        {
            "role": "roles/viewer",
            "members": [
                "serviceAccount:test-service-account@test-project-id.iam.gserviceaccount.com",
            ],
        },
    ]
    role = "roles/viewer"
    member = "allAuthenticatedUsers"

    modify_policy_add_member(project_id, bindings, role, member)
