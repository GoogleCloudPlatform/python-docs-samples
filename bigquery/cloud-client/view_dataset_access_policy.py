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

from google.cloud.bigquery.dataset import Dataset


def view_dataset_access_policy(dataset_id: str) -> Dataset:
    # [START bigquery_view_dataset_access_policy]
    # Imports the Google Cloud client library
    from google.cloud import bigquery

    # Instantiates a client
    bigquery_client = bigquery.Client()

    # TODO(developer): Update and un-comment below lines
    # Dataset from which to get the access policy
    # dataset_id = "my_new_dataset"

    # Prepares a reference to the dataset
    dataset = bigquery_client.get_dataset(dataset_id)

    # Shows the Access policy as a list of Access Entries
    print(dataset.access_entries)

    # More details about AccessEntry object here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry

    # Get properties for an AccessEntry
    if dataset.access_entries:
        print(f"Details for Access entry 0 in dataset '{dataset_id}'.")
        print(f"Role: {dataset.access_entries[0].role}")
        print(f"Special group: {dataset.access_entries[0].special_group}")
        print(f"User by Email: {dataset.access_entries[0].user_by_email}")
    # [END bigquery_view_dataset_access_policy]

    return dataset
