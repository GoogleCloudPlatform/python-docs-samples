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

# [START iam_service_account_get_policy]
from google.cloud import iam_admin_v1
from google.iam.v1 import iam_policy_pb2, policy_pb2


def get_service_account_iam_policy(project_id: str, account: str) -> policy_pb2.Policy:
    """Get policy for service account.

    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    """

    iam_client = iam_admin_v1.IAMClient()
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = f"projects/{project_id}/serviceAccounts/{account}"

    policy = iam_client.get_iam_policy(request)
    return policy
# [END iam_service_account_get_policy]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccounts.getIamPolicy permission (roles/iam.serviceAccountAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    # Existing service account name within the project specified above.
    name = "test-account-name"
    service_account = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"

    policy = get_service_account_iam_policy(PROJECT_ID, service_account)
    print(policy)
