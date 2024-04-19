# Copyright 2022 Google LLC
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

# This file contains code samples that demonstrate how to get create IAM key for service account.


# [START iam_get_policy]
def get_policy(project_id: str, service_account, account: str = None, policy_id: str = None) -> str:
    from google.cloud import iam_admin_v1
    from google.iam.v1 import iam_policy_pb2
    """
    Get IAM policies for service account
    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    """

    iam_client = iam_admin_v1.IAMClient()

    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = f"projects/{project_id}/serviceAccounts/{service_account}"

    response = iam_client.get_iam_policy(request)
    print(response)


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccountKeys.create permission (roles/iam.serviceAccountKeyAdmin)

    # Your Google Cloud project ID.
    project_id = "test-project-id"
    name = "test-account-name"
    service_account = f"{name}@{project_id}.iam.gserviceaccount.com"

    get_policy(project_id, service_account)

# [END iam_get_policy]