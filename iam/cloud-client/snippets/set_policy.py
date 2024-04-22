# Copyright 2022 Google LLC
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

# This file contains code samples that demonstrate how to set policy for service account.

# [START iam_serivce_account_set_policy]
from google.cloud import iam_admin_v1
from google.iam.v1 import iam_policy_pb2, policy_pb2


def set_policy(project_id: str, account: str) -> policy_pb2.Policy:
    """
    Set policy for service account.
    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    """

    iam_client = iam_admin_v1.IAMClient()
    request = iam_policy_pb2.SetIamPolicyRequest()

    binding = policy_pb2.Binding()
    # Role, which will be assigned to an entity
    binding.role = "roles/iam.serviceAccountTokenCreator"

    # Prefix specifies the principals requesting access for a Google Cloud resource.
    # `members` can have the following values:
    #
    # * `allUsers`: A special identifier that represents anyone who is
    #    on the internet; with or without a Google account.
    #
    # * `allAuthenticatedUsers`: A special identifier that represents anyone
    #    who is authenticated with a Google account or a service account.
    #
    # * `user:{emailid}`: An email address that represents a specific Google
    #    account. For example, `alice@example.com` .
    #
    #
    # * `serviceAccount:{emailid}`: An email address that represents a service
    #    account. For example, `my-other-app@appspot.gserviceaccount.com`.
    #
    # * `group:{emailid}`: An email address that represents a Google group.
    #    For example, `admins@example.com`.
    #
    # * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique
    #    identifier) representing a user that has been recently deleted. For
    #    example, `alice@example.com?uid=123456789012345678901`. If the user is
    #    recovered, this value reverts to `user:{emailid}` and the recovered user
    #    retains the role in the binding.
    #
    # * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus
    #    unique identifier) representing a service account that has been recently
    #    deleted. For example,
    #    `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`.
    #    If the service account is undeleted, this value reverts to
    #    `serviceAccount:{emailid}` and the undeleted service account retains the
    #    role in the binding.
    #
    # * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique
    #    identifier) representing a Google group that has been recently
    #    deleted. For example, `admins@example.com?uid=123456789012345678901`. If
    #    the group is recovered, this value reverts to `group:{emailid}` and the
    #    recovered group retains the role in the binding.
    #
    # * `domain:{domain}`: The G Suite domain (primary) that represents all the
    #    users of that domain. For example, `google.com` or `example.com`.
    binding.members.append(f"serviceAccount:{account}")

    # Optional example of condition (available starting from 3 version of Policy)
    # For more details visit https://cloud.google.com/iam/docs/conditions-overview
    binding.condition.title = "Compute only"
    binding.condition.description = "Apply policy only for compute"
    binding.condition.expression = "request.time < timestamp('2018-08-03T16:00:00-07:00')"

    request.resource = f"projects/{project_id}/serviceAccounts/{account}"
    request.policy.bindings.append(binding)
    request.policy.version = 2

    policy = iam_client.set_iam_policy(request)
    return policy

# [END iam_serivce_account_set_policy]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccounts.getIamPolicy permission (roles/iam.serviceAccountAdmin)

    # Your Google Cloud project ID.

    project_id = "test-project-id"
    # Existing service account name within the project specified above.
    name = "test-account-name"

    project_id = "gcp103148-cloudaccount"
    # Existing service account name within the project specified above.
    name = "test-access-key"

    service_account = f"{name}@{project_id}.iam.gserviceaccount.com"

    set_policy(project_id, service_account)
