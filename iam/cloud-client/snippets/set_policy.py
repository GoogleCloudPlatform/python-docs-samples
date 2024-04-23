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

# [START iam_set_policy]
from typing import Dict, List, Union

from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2


def set_policy(
    project_id: str, bindings: List[Dict[str, Union[str, List[str]]]]
) -> policy_pb2.Policy:
    """
    Set policy for project. Pay attention that previous state will be completely rewritten.
    If you want to update only part of the policy leverage update_policy snippet.
    For more details about policies check out https://cloud.google.com/iam/docs/policies

    project_id: ID or number of the Google Cloud project you want to use.
    bindings: List of bindings, which contains all policies for the project.

    Bindings example:
    [
        {
            "role": "roles/viewer",
            "members": [
                "serviceAccount:test-service-account@test-project-id.iam.gserviceaccount.com",
            ],
        },
    ]
    """

    client = resourcemanager_v3.ProjectsClient()
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = f"projects/{project_id}"

    set_bindings = []
    for bind in bindings:
        binding = policy_pb2.Binding()
        binding.role = bind["role"]
        binding.members.extend(bind["members"])
        set_bindings.append(binding)

    request.policy.bindings.extend(set_bindings)
    policy = client.set_iam_policy(request)
    return policy


# [END iam_set_policy]


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
            "condition": {},
        },
    ]

    set_policy(project_id, bindings)
