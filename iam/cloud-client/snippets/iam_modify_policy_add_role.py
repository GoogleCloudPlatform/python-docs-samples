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


# [START iam_modify_policy_add_role]
def modify_policy_add_role(policy: dict, role: str, principal: str) -> dict:
    """Adds a new role binding to a policy."""

    binding = {"role": role, "members": [principal]}
    policy["bindings"].append(binding)
    print(policy)
    return policy
# [END iam_modify_policy_add_role]
