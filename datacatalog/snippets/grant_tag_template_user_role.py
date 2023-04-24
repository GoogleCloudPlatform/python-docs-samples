# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def grant_tag_template_user_role(override_values):
    """Grants a user the Tag Template User role for a given template."""
    # [START data_catalog_grant_tag_template_user_role]
    from google.cloud import datacatalog_v1
    from google.iam.v1 import iam_policy_pb2 as iam_policy
    from google.iam.v1 import policy_pb2

    datacatalog = datacatalog_v1.DataCatalogClient()

    # TODO: Set these values before running the sample.
    project_id = "project_id"
    tag_template_id = "existing_tag_template_id"
    # For a full list of values a member can have, see:
    # https://cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=en#binding
    member_id = "user:super-cool.test-user@gmail.com"

    # [END data_catalog_grant_tag_template_user_role]

    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    tag_template_id = override_values.get("tag_template_id", tag_template_id)
    member_id = override_values.get("member_id", member_id)

    # [START data_catalog_grant_tag_template_user_role]
    # For all regions available, see:
    # https://cloud.google.com/data-catalog/docs/concepts/regions
    location = "us-central1"

    # Format the Template name.
    template_name = datacatalog_v1.DataCatalogClient.tag_template_path(
        project_id, location, tag_template_id
    )

    # Retrieve Template's current IAM Policy.
    policy = datacatalog.get_iam_policy(resource=template_name)

    # Add Tag Template User role and member to the policy.
    binding = policy_pb2.Binding()
    binding.role = "roles/datacatalog.tagTemplateUser"
    binding.members.append(member_id)
    policy.bindings.append(binding)

    set_policy_request = iam_policy.SetIamPolicyRequest(
        resource=template_name, policy=policy
    )

    # Update Template's policy.
    policy = datacatalog.set_iam_policy(set_policy_request)

    for binding in policy.bindings:
        for member in binding.members:
            print(f"Member: {member}, Role: {binding.role}")
    # [END data_catalog_grant_tag_template_user_role]
