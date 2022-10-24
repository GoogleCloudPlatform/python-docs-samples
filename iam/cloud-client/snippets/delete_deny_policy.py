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

# This file contains code samples that demonstrate how to delete IAM deny policies.

# [START iam_delete_deny_policy]
def delete_deny_policy(project_id: str, policy_id: str) -> None:
    from google.cloud import iam_v2
    from google.cloud.iam_v2 import types

    """
    Delete the policy if you no longer want to enforce the rules in a deny policy.

    project_id: ID or number of the Google Cloud project you want to use.
    policy_id: The ID of the deny policy you want to retrieve.
    """
    policies_client = iam_v2.PoliciesClient()

    # Each deny policy is attached to an organization, folder, or project.
    # To work with deny policies, specify the attachment point.
    #
    # Its format can be one of the following:
    # 1. cloudresourcemanager.googleapis.com/organizations/ORG_ID
    # 2. cloudresourcemanager.googleapis.com/folders/FOLDER_ID
    # 3. cloudresourcemanager.googleapis.com/projects/PROJECT_ID
    #
    # The attachment point is identified by its URL-encoded resource name. Hence, replace
    # the "/" with "%2F".
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = types.DeletePolicyRequest()
    # Construct the full path of the policy.
    # Its format is: "policies/{attachmentPoint}/denypolicies/{policyId}"
    request.name = f"policies/{attachment_point}/denypolicies/{policy_id}"

    # Create the DeletePolicy request.
    result = policies_client.delete_policy(request=request).result()
    print(f"Deleted the deny policy: {result.name.rsplit('/')[-1]}")


if __name__ == "__main__":
    import uuid

    # Your Google Cloud project ID.
    project_id = "your-google-cloud-project-id"
    # Any unique ID (0 to 63 chars) starting with a lowercase letter.
    policy_id = f"deny-{uuid.uuid4()}"

    delete_deny_policy(project_id, policy_id)

# [END iam_delete_deny_policy]
