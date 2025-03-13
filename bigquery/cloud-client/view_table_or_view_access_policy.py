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


def view_table_or_view_access_policy(project_id: str, dataset_id: str, resource_id: str) -> Policy:
    # [START bigquery_view_table_or_view_access_policy]
    from google.cloud import bigquery

    # TODO(developer): Update and uncomment the lines below.

    # Google Cloud Platform project.
    # project_id = "my_project_id"

    # Dataset where the table or view is.
    # dataset_id = "my_dataset_id"

    # Table or view from which to get the access policy.
    # resource_id = "my_table_id"

    # Instantiate a client.
    client = bigquery.Client()

    # Get the full table or view id.
    full_resource_id = f"{project_id}.{dataset_id}.{resource_id}"

    # Get the IAM access policy for the table or view.
    policy = client.get_iam_policy(full_resource_id)

    # Show policy details.
    # Find more details for the Policy object here:
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Policy
    print(f"Access Policy details for table or view '{resource_id}'.")
    print(f"Bindings: {policy.bindings}")
    print(f"etag: {policy.etag}")
    print(f"Version: {policy.version}")
    # [END bigquery_view_table_or_view_access_policy]

    return policy
