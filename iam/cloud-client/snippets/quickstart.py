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


# [START iam_quickstart]
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2


def quickstart(project_id: str, principal: str) -> None:
    """Demonstrates basic IAM operations.

    This quickstart shows how to get a project's IAM policy,
    add a principal to a role, list members of a role,
    and remove a principal from a role.

    Args:
        project_id: ID or number of the Google Cloud project you want to use.
        principal: The principal ID requesting the access.
    """

    # Role to be granted.
    role = "roles/logging.logWriter"
    crm_service = resourcemanager_v3.ProjectsClient()

    # Grants your principal the 'Log Writer' role for the project.
    modify_policy_add_role(crm_service, project_id, role, principal)

    # Gets the project's policy and prints all principals with the 'Log Writer' role.
    policy = get_policy(crm_service, project_id)
    binding = next(b for b in policy.bindings if b.role == role)
    print(f"Role: {(binding.role)}")
    print("Members: ")
    for m in binding.members:
        print(f"[{m}]")

    # Removes the principal from the 'Log Writer' role.
    modify_policy_remove_principal(crm_service, project_id, role, principal)


def get_policy(
    crm_service: resourcemanager_v3.ProjectsClient, project_id: str
) -> policy_pb2.Policy:
    """Gets IAM policy for a project."""

    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = f"projects/{project_id}"

    policy = crm_service.get_iam_policy(request)
    return policy


def set_policy(
    crm_service: resourcemanager_v3.ProjectsClient,
    project_id: str,
    policy: policy_pb2.Policy,
) -> None:
    """Adds a new role binding to a policy."""

    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = f"projects/{project_id}"
    request.policy.CopyFrom(policy)

    crm_service.set_iam_policy(request)


def modify_policy_add_role(
    crm_service: resourcemanager_v3.ProjectsClient,
    project_id: str,
    role: str,
    principal: str,
) -> None:
    """Adds a new role binding to a policy."""

    policy = get_policy(crm_service, project_id)

    for bind in policy.bindings:
        if bind.role == role:
            bind.members.append(principal)
            break
    else:
        binding = policy_pb2.Binding()
        binding.role = role
        binding.members.append(principal)
        policy.bindings.append(binding)

    set_policy(crm_service, project_id, policy)


def modify_policy_remove_principal(
    crm_service: resourcemanager_v3.ProjectsClient,
    project_id: str,
    role: str,
    principal: str,
) -> None:
    """Removes a principal from a role binding."""

    policy = get_policy(crm_service, project_id)

    for bind in policy.bindings:
        if bind.role == role:
            if principal in bind.members:
                bind.members.remove(principal)
            break

    set_policy(crm_service, project_id, policy)


if __name__ == "__main__":
    # TODO: Replace with your project ID.
    project_id = "your-project-id"
    # TODO: Replace with the ID of your principal.
    # For examples, see https://cloud.google.com/iam/docs/principal-identifiers
    principal = "your-principal"
    quickstart(project_id, principal)
# [END iam_quickstart]
