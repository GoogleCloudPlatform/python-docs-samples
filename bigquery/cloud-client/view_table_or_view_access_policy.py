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

import os
from typing import Dict, Optional

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def view_table_or_view_access_policy(override_values: Optional[Dict[str, str]] = None) -> None:
    if override_values is None:
        override_values = {}

    # [START bigquery_view_table_or_view_access_policy]
    # Imports the Google Cloud client library
    from google.cloud import bigquery

    # TODO: Set these values before running the sample.
    # Google Cloud Platform project.
    project_id = "my_project_id"
    # Dataset where the table or view is.
    dataset_id = "my_new_dataset"
    # Table or view name to get the access policy.
    resource_name = "my_table"

    # [END bigquery_view_table_or_view_access_policy]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = PROJECT_ID
    dataset_id = override_values.get("dataset_id", dataset_id)
    resource_name = override_values.get("resource_name", resource_name)
    # [START bigquery_view_table_or_view_access_policy]

    # Instantiates a client.
    bigquery_client = bigquery.Client()

    # Get the full table name.
    full_resource_name = f"{project_id}.{dataset_id}.{resource_name}"

    # Get the IAM access policy for the table or view.
    policy = bigquery_client.get_iam_policy(full_resource_name)

    # Show policy details.
    # Find more details for the Policy object here:
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Policy
    print(f"Access Policy details for table or view '{resource_name}'.")
    print(f"Bindings: {policy.bindings}")
    print(f"etag: {policy.etag}")
    print(f"Version: {policy.version}")
    # [END bigquery_view_table_or_view_access_policy]


if __name__ == "__main__":
    view_table_or_view_access_policy()
