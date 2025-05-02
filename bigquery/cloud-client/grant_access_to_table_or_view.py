# Copyright 2024 Google LLC
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

from google.api_core.iam import Policy


def grant_access_to_table_or_view(
    project_id: str,
    dataset_id: str,
    resource_name: str,
    principal_id: str,
    role: str,
) -> Policy:

    # [START bigquery_grant_access_to_table_or_view]
    from google.cloud import bigquery

    # TODO(developer): Update and uncomment the lines below.

    # Google Cloud Platform project.
    # project_id = "my_project_id"

    # Dataset where the table or view is.
    # dataset_id = "my_dataset"

    # Table or view name to get the access policy.
    # resource_name = "my_table"

    # Principal to grant access to a table or view.
    # For more information about principal identifiers see:
    # https://cloud.google.com/iam/docs/principal-identifiers
    # principal_id = "user:bob@example.com"

    # Role to grant to the principal.
    # For more information about BigQuery roles see:
    # https://cloud.google.com/bigquery/docs/access-control
    # role = "roles/bigquery.dataViewer"

    # Instantiate a client.
    client = bigquery.Client()

    # Get the full table or view name.
    full_resource_name = f"{project_id}.{dataset_id}.{resource_name}"

    # Get the IAM access policy for the table or view.
    policy = client.get_iam_policy(full_resource_name)

    # To grant access to a table or view, add bindings to the IAM policy.
    #
    # Find more details about Policy and Binding objects here:
    # https://cloud.google.com/security-command-center/docs/reference/rest/Shared.Types/Policy
    # https://cloud.google.com/security-command-center/docs/reference/rest/Shared.Types/Binding
    binding = {
        "role": role,
        "members": [principal_id, ],
    }
    policy.bindings.append(binding)

    # Set the IAM access policy with updated bindings.
    updated_policy = client.set_iam_policy(full_resource_name, policy)

    # Show a success message.
    print(
        f"Role '{role}' granted for principal '{principal_id}'"
        f" on resource '{full_resource_name}'."
    )
    # [END bigquery_grant_access_to_table_or_view]

    return updated_policy.bindings
