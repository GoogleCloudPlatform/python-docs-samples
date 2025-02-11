#!/usr/bin/env python

# Copyright 2025 Google Inc. All Rights Reserved.
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

from typing import Dict, Optional


def view_dataset_access_policies(override_values: Optional[Dict[str, str]] = None) -> None:
    if override_values is None:
        override_values = {}

    # [START bigquery_view_dataset_access_policies]
    # Imports the Google Cloud client library
    from google.cloud import bigquery

    # Instantiates a client
    bigquery_client = bigquery.Client()

    # Dataset from which to get access policies
    dataset_id = "my_new_dataset"

    # [END bigquery_view_dataset_access_policies]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    dataset_id = override_values.get("dataset_id", dataset_id)
    # [START bigquery_view_dataset_access_policies]

    # Prepares a reference to the dataset
    dataset = bigquery_client.get_dataset(dataset_id)

    # Shows a list of Access Entries for this dataset
    print(dataset.access_entries)

    # More details about AccessEntry objects here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry

    # Get properties for an AccessEntry
    print("Access entry 0 - Role: '{}'.".format(dataset.access_entries[0].role))
    print("Access entry 0 - Special group: '{}'.".format(dataset.access_entries[0].special_group))
    print("Access entry 0 - User by Email: '{}'.".format(dataset.access_entries[0].user_by_email))
    # [END bigquery_view_dataset_access_policies]


if __name__ == "__main__":
    view_dataset_access_policies()
