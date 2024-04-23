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
from typing import Dict, List, Union


def modify_policy_remove_member(
    bindings: List[Dict[str, Union[str, List[str]]]], role: str, member: str
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Remove user from policy binding.

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
    for bind in bindings:
        if bind["role"] == role:
            if member in bind["members"]:
                bind["members"].remove(member)

    return bindings

# [END iam_modify_policy_remove_member]


if __name__ == "__main__":
    role = "roles/viewer"
    bindings = [
        {
            "role": role,
            "members": [
                "serviceAccount:test-service-account@test-project-id.iam.gserviceaccount.com",
            ],
        },
    ]
    member = "serviceAccount:test-service-account@test-project-id.iam.gserviceaccount.com"

    modify_policy_remove_member(bindings, role, member)
