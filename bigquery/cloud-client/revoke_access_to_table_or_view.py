#!/usr/bin/env python

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
    # dataset_id = "my_new_dataset"
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
    # For this example remove all bindings for the role 'dataViewer'.
    role_to_remove = "roles/bigquery.dataViewer"

    # Create a new list removing all bindings for role 'dataViewer'
    policy.bindings = [b for b in policy.bindings if b["role"] != role_to_remove]

    print(policy.bindings)  # DEBUG: Check that we've removed the bindings
    new_policy = bigquery_client.set_iam_policy(full_resource_name, policy)
    print(new_policy.bindings)  # DEBUG: Check that the new policy is right

    print(f"Role '{role_to_remove}' has been revoked from '{full_resource_name}'")
    # [END bigquery_revoke_access_to_table_or_view]

    # Minor detail to discuss:
    # Although the library documentation says that bindings
    # may be returned as a dict, looking into the source code
    # I can only see it being returned as a list, which results
    # in a different logic than on Java which uses a HashMap/Dictionary
    # https://github.com/googleapis/python-api-core/blob/7fbd5fda207d856b5835d0e0166df52e4819522a/google/api_core/iam.py#L189-L190

    # Java code this sample is based on:
    # Map<Role, Set<Identity>> binding = new HashMap<>(policy.getBindings());
    # binding.remove(Role.of("roles/bigquery.dataViewer"));
    #
    # policy.toBuilder().setBindings(binding).build();
    # bigquery.setIamPolicy(tableId, policy);
    #
    # System.out.println("Iam policy updated successfully");

    # Get the policy again for testing purposes
    new_policy = bigquery_client.get_iam_policy(full_resource_name)
    return new_policy


table_policy = revoke_access_to_table_or_view(
    "samples-xwf-01",
    "my_new_dataset",
    "my_table"
)
print(table_policy.bindings)
