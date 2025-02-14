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

from google.api_core.iam import Policy


def revoke_access_to_table_or_view(project_id: str, dataset_id: str, resource_name: str) -> Policy:
    # [START bigquery_revoke_access_to_table_or_view]
    # Imports the Google Cloud client library
    from google.cloud import bigquery

    # TODO(developer): Update and un-comment below lines
    # Google Cloud Platform project.
    # project_id = "my_project_id"
    # Dataset where the table or view is.
    # dataset_id = "my_dataset"
    # Table or view name to get the access policy.
    # resource_name = "my_table"

    # Instantiates a client.
    bigquery_client = bigquery.Client()

    # Get the full table name.
    full_resource_name = f"{project_id}.{dataset_id}.{resource_name}"

    # Get the IAM access policy for the table or view.
    policy = bigquery_client.get_iam_policy(full_resource_name)

    print(policy.bindings)  # DEBUG: Show the binding list before making changes

    # To revoke access to a table or view,
    # remove bindings from the Table or View policy.
    # You may remove a binding by role or by principal.
    #
    # Find more details about Policy and Bindings objects here:
    # https://cloud.google.com/security-command-center/docs/reference/rest/Shared.Types/Policy
    # https://cloud.google.com/security-command-center/docs/reference/rest/Shared.Types/Binding

    # For this example remove all bindings for the role 'dataViewer'.
    role_to_remove = "roles/bigquery.dataViewer"

    # Create a new list removing all bindings for role 'dataViewer'
    # and assign it back to the policy.
    policy.bindings = [b for b in policy.bindings if b["role"] != role_to_remove]

    new_policy = bigquery_client.set_iam_policy(full_resource_name, policy)

    print(f"Role '{role_to_remove}' has been revoked from '{full_resource_name}'")
    # [END bigquery_revoke_access_to_table_or_view]

    # Get the policy again for testing purposes
    new_policy = bigquery_client.get_iam_policy(full_resource_name)
    return new_policy
