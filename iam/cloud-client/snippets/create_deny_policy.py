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

# This file contains code samples that demonstrate how to create IAM deny policies.

# [START iam_create_deny_policy]


def create_deny_policy(project_id: str, policy_id: str) -> None:
    from google.cloud import iam_v2
    from google.cloud.iam_v2 import types

    """
      Create a deny policy.
      You can add deny policies to organizations, folders, and projects.
      Each of these resources can have up to 5 deny policies.

      Deny policies contain deny rules, which specify the following:
      1. The permissions to deny and/or exempt.
      2. The principals that are denied, or exempted from denial.
      3. An optional condition on when to enforce the deny rules.

      Params:
      project_id: ID or number of the Google Cloud project you want to use.
      policy_id: Specify the ID of the deny policy you want to create.
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

    # Optionally, set the principals who should be exempted from the
    # list of denied principals. For example, if you want to deny certain permissions
    # to a group but exempt a few principals, then add those here.
    # deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]

    # Set the permissions to deny.
    # The permission value is of the format: service_fqdn/resource.action
    # For the list of supported permissions, see: https://cloud.google.com/iam/help/deny/supported-permissions
    deny_rule.denied_permissions = [
        "cloudresourcemanager.googleapis.com/projects.delete"
    ]

    # Optionally, add the permissions to be exempted from this rule.
    # Meaning, the deny rule will not be applicable to these permissions.
    # deny_rule.exception_permissions = ["cloudresourcemanager.googleapis.com/projects.create"]

    # Set the condition which will enforce the deny rule.
    # If this condition is true, the deny rule will be applicable. Else, the rule will not be enforced.
    # The expression uses Common Expression Language syntax (CEL).
    # Here we block access based on tags.
    #
    # Here, we create a deny rule that denies the cloudresourcemanager.googleapis.com/projects.delete permission to everyone except project-admins@example.com for resources that are tagged test.
    # A tag is a key-value pair that can be attached to an organization, folder, or project.
    # For more info, see: https://cloud.google.com/iam/docs/deny-access#create-deny-policy
    deny_rule.denial_condition = {
        "expression": "!resource.matchTag('12345678/env', 'test')"
    }

    # Add the deny rule and a description for it.
    policy_rule = types.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value test"
    policy_rule.deny_rule = deny_rule

    policy = types.Policy()
    policy.display_name = "Restrict project deletion access"
    policy.rules = [policy_rule]

    # Set the policy resource path, policy rules and a unique ID for the policy.
    request = types.CreatePolicyRequest()
    # Construct the full path of the resource's deny policies.
    # Its format is: "policies/{attachmentPoint}/denypolicies"
    request.parent = f"policies/{attachment_point}/denypolicies"
    request.policy = policy
    request.policy_id = policy_id

    # Build the create policy request and wait for the operation to complete.
    result = policies_client.create_policy(request=request).result()
    print(f"Created the deny policy: {result.name.rsplit('/')[-1]}")


if __name__ == "__main__":
    import uuid

    # Your Google Cloud project ID.
    project_id = "your-google-cloud-project-id"
    # Any unique ID (0 to 63 chars) starting with a lowercase letter.
    policy_id = f"deny-{uuid.uuid4()}"

    # Test the policy lifecycle.
    create_deny_policy(project_id, policy_id)

# [END iam_create_deny_policy]
