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

from google.cloud.bigquery.dataset import AccessEntry


def view_dataset_access_policy(dataset_id: str) -> list[AccessEntry]:
    # [START bigquery_view_dataset_access_policy]
    from google.cloud import bigquery

    # Instantiate a client.
    client = bigquery.Client()

    # TODO(developer): Update and uncomment the lines below.

    # Dataset from which to get the access policy.
    # dataset_id = "my_dataset"

    # Get a reference to the dataset.
    dataset = client.get_dataset(dataset_id)

    # Show the list of AccessEntry objects.
    # More details about the AccessEntry object here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry
    print(
        f"{len(dataset.access_entries)} Access entries found "
        f"in dataset '{dataset_id}':"
    )

    for access_entry in dataset.access_entries:
        print()
        print(f"Role: {access_entry.role}")
        print(f"Special group: {access_entry.special_group}")
        print(f"User by Email: {access_entry.user_by_email}")
    # [END bigquery_view_dataset_access_policy]

    return dataset.access_entries
