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

# This file contains code samples that demonstrate how to update IAM deny policies.

# [START iam_update_deny_policy]
def update_deny_policy(project_id: str, policy_id: str, etag: str) -> None:
    from google.cloud import iam_v2
    from google.cloud.iam_v2 import types

    """
    Update the deny rules and/ or its display name after policy creation.

    project_id: ID or number of the Google Cloud project you want to use.

    policy_id: The ID of the deny policy you want to retrieve.

    etag: Etag field that identifies the policy version. The etag changes each time
    you update the policy. Get the etag of an existing policy by performing a GetPolicy request.
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

    deny_rule = types.DenyRule()

    # Add one or more principals who should be denied the permissions specified in this rule.
    # For more information on allowed values, see: https://cloud.google.com/iam/help/deny/principal-identifiers
    deny_rule.denied_principals = ["principalSet://goog/public:all"]

    # Optionally, set the principals who should be exempted from the list of principals added in "DeniedPrincipals".
    # Example, if you want to deny certain permissions to a group but exempt a few principals, then add those here.
    # deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]

    # Set the permissions to deny.
    # The permission value is of the format: service_fqdn/resource.action
    # For the list of supported permissions, see: https://cloud.google.com/iam/help/deny/supported-permissions
    deny_rule.denied_permissions = [
        "cloudresourcemanager.googleapis.com/projects.delete"
    ]

    # Add the permissions to be exempted from this rule.
    # Meaning, the deny rule will not be applicable to these permissions.
    # deny_rule.exception_permissions = ["cloudresourcemanager.googleapis.com/projects.get"]

    # Set the condition which will enforce the deny rule.
    # If this condition is true, the deny rule will be applicable. Else, the rule will not be enforced.
    #
    # The expression uses Common Expression Language syntax (CEL). Here we block access based on tags.
    #
    # Here, we create a deny rule that denies the cloudresourcemanager.googleapis.com/projects.delete permission to everyone except project-admins@example.com for resources that are tagged prod.
    # A tag is a key-value pair that can be attached to an organization, folder, or project.
    # For more info, see: https://cloud.google.com/iam/docs/deny-access#create-deny-policy
    deny_rule.denial_condition = {
        "expression": "!resource.matchTag('12345678/env', 'prod')"
    }

    # Set the rule description and deny rule to update.
    policy_rule = types.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value prod"
    policy_rule.deny_rule = deny_rule

    # Set the policy resource path, version (etag) and the updated deny rules.
    policy = types.Policy()
    # Construct the full path of the policy.
    # Its format is: "policies/{attachmentPoint}/denypolicies/{policyId}"
    policy.name = f"policies/{attachment_point}/denypolicies/{policy_id}"
    policy.etag = etag
    policy.rules = [policy_rule]

    # Create the update policy request.
    request = types.UpdatePolicyRequest()
    request.policy = policy

    result = policies_client.update_policy(request=request).result()
    print(f"Updated the deny policy: {result.name.rsplit('/')[-1]}")


if __name__ == "__main__":
    import uuid

    # Your Google Cloud project ID.
    project_id = "your-google-cloud-project-id"
    # Any unique ID (0 to 63 chars) starting with a lowercase letter.
    policy_id = f"deny-{uuid.uuid4()}"
    # Get the etag by performing a Get policy request.
    etag = "etag"

    update_deny_policy(project_id, policy_id, etag)

# [END iam_update_deny_policy]
