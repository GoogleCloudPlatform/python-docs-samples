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

# This file contains code samples that demonstrate how to get policy for service account.

# [START iam_service_account_get_policy]
from google.cloud import iam_admin_v1
from google.iam.v1 import iam_policy_pb2, policy_pb2
from google.cloud import resourcemanager_v3


def get_policy(project_id: str, account: str) -> policy_pb2.Policy:
    """
    Get policy for service account.
    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    """

    # iam_client = iam_admin_v1.IAMClient()
    # request = iam_policy_pb2.GetIamPolicyRequest()
    # request.resource = f"projects/{project_id}/serviceAccounts/{account}"

    # policy = iam_client.get_iam_policy(request)
    # print(policy)
    # return policy

    client = resourcemanager_v3.ProjectsClient()
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = f"projects/{project_id}"

    policy = client.get_iam_policy(request)
    print(policy)
    return policy

# [END iam_service_account_get_policy]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccounts.getIamPolicy permission (roles/iam.serviceAccountAdmin)

    # Your Google Cloud project ID.
    project_id = "test-project-id"
    # Existing service account name within the project specified above.
    name = "test-account-name"
    service_account = f"{name}@{project_id}.iam.gserviceaccount.com"

    project_id = "gcp103148-cloudaccount"
    # Existing service account name within the project specified above.
    name = "test-access-key"
    service_account = f"{name}@{project_id}.iam.gserviceaccount.com"

    get_policy(project_id, service_account)


# import os

# from google.oauth2 import service_account  # type: ignore
# import googleapiclient.discovery  # type: ignore


# # [START iam_get_policy]
# def get_policy(project_id: str, version: int = 1) -> dict:
#     """Gets IAM policy for a project."""

#     credentials = service_account.Credentials.from_service_account_file(
#         filename="/Users/srasp/.config/gcloud/application_default_credentials2.json",
#         scopes=["https://www.googleapis.com/auth/cloud-platform"],
#     )
#     service = googleapiclient.discovery.build(
#         "cloudresourcemanager", "v1", credentials=credentials
#     )
#     policy = (
#         service.projects()
#         .getIamPolicy(
#             resource=project_id,
#             body={"options": {"requestedPolicyVersion": version}},
#         )
#         .execute()
#     )
#     print(policy)
#     return policy

# get_policy("gcp103148-cloudaccount")