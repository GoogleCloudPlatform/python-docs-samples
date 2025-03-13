# Copyright 2025 Google LLC
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

from __future__ import annotations

from google.api_core.iam import Policy


def revoke_access_to_table_or_view(
    project_id: str,
    dataset_id: str,
    resource_name: str,
    role_to_remove: str | None = None,
    principal_to_remove: str | None = None,
) -> Policy:
    # [START bigquery_revoke_access_to_table_or_view]
    from google.cloud import bigquery

    # TODO(developer): Update and uncomment the lines below.

    # Google Cloud Platform project.
    # project_id = "my_project_id"

    # Dataset where the table or view is.
    # dataset_id = "my_dataset"

    # Table or view name to get the access policy.
    # resource_name = "my_table"

    # (Optional) Role to remove from the table or view.
    # role_to_remove = "roles/bigquery.dataViewer"

    # (Optional) Principal to revoke access to the table or view.
    # principal_to_remove = "user:alice@example.com"

    # Find more information about roles and principals (referred to as members) here:
    # https://cloud.google.com/security-command-center/docs/reference/rest/Shared.Types/Binding

    # Instantiate a client.
    client = bigquery.Client()

    # Get the full table name.
    full_resource_name = f"{project_id}.{dataset_id}.{resource_name}"

    # Get the IAM access policy for the table or view.
    policy = client.get_iam_policy(full_resource_name)

    # To revoke access to a table or view,
    # remove bindings from the Table or View IAM policy.
    #
    # Find more details about the Policy object here:
    # https://cloud.google.com/security-command-center/docs/reference/rest/Shared.Types/Policy

    if role_to_remove:
        # Filter out all bindings with the `role_to_remove`
        # and assign a new list back to the policy bindings.
        policy.bindings = [b for b in policy.bindings if b["role"] != role_to_remove]

    if principal_to_remove:
        # The `bindings` list is immutable. Create a copy for modifications.
        bindings = list(policy.bindings)

        # Filter out the principal for each binding.
        for binding in bindings:
            binding["members"] = [m for m in binding["members"] if m != principal_to_remove]

        # Assign back the modified binding list.
        policy.bindings = bindings

    new_policy = client.set_iam_policy(full_resource_name, policy)
    # [END bigquery_revoke_access_to_table_or_view]

    # Get the policy again for testing purposes
    new_policy = client.get_iam_policy(full_resource_name)
    return new_policy
