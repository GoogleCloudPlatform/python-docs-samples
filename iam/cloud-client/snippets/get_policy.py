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
def get_policy(project_id: str, account: str = None, policy_id: str = None) -> str:
    from google.cloud import iam_admin_v1
    from google.cloud.iam_admin_v1 import types
    """
    Creates a key for a service account.
    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    """

    # policy_client = iam_v2.PoliciesClient()
    # request = types.GetPolicyRequest()
    # attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2{project_id}"
    # request.name = f"policies/{attachment_point}/denypolicies/{policy_id}"

    # policy = iam_admin_client.get_policy(request=request)
    # print(policy)

    import pdb;pdb.set_trace()
    iam_client = iam_admin_v1.IAMClient()

    request = types.GetIamPolicyRequest()
    request.resource = project_id

    response = iam_client.get_iam_policy(request)
    print(response)


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccountKeys.create permission (roles/iam.serviceAccountKeyAdmin)

    # Your Google Cloud project ID.
    project_id = "srasp-softserve-project"

    get_policy(project_id)

# [END iam_get_policy]