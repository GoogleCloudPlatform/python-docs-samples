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

import os

# [START iam_service_account_set_policy]
from google.cloud import iam_admin_v1
from google.iam.v1 import iam_policy_pb2, policy_pb2


def set_service_account_iam_policy(
    project_id: str, account: str, policy: policy_pb2.Policy
) -> policy_pb2.Policy:
    """Set policy for service account.

    Pay attention that previous state will be completely rewritten.
    If you want to update only part of the policy follow the approach
    read->modify->write.
    For more details about policies check out
    https://cloud.google.com/iam/docs/policies

    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    policy: Policy which has to be set.
    """

    # Same approach as for policies on project level,
    # but client stub is different.
    iam_client = iam_admin_v1.IAMClient()
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = f"projects/{project_id}/serviceAccounts/{account}"

    # request.etag field also will be merged which means
    # you are secured from collision, but it means that request
    # may fail and you need to leverage exponential retries approach
    # to be sure policy has been updated.
    request.policy.MergeFrom(policy)

    policy = iam_client.set_iam_policy(request)
    return policy
# [END iam_service_account_set_policy]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccounts.setIamPolicy permission (roles/iam.serviceAccountAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    # Existing service account name within the project specified above.
    name = "test-account-name"
    service_account = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"

    policy = policy_pb2.Policy()
    role = "roles/viewer"
    test_binding = policy_pb2.Binding()
    test_binding.role = role
    test_binding.members.extend(
        [
            f"serviceAccount:{PROJECT_ID}@appspot.gserviceaccount.com",
        ]
    )
    policy.bindings.append(test_binding)

    set_service_account_iam_policy(PROJECT_ID, service_account, policy)
