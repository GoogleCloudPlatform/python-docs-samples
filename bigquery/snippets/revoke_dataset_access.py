# Copyright 2021 Google LLC
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


def revoke_dataset_access(dataset_id: str, entity_id: str):
    original_dataset_id = dataset_id
    original_entity_id = entity_id

    # [START bigquery_revoke_dataset_access]

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    dataset_id = "your-project.your_dataset"

    # TODO(developer): Set entity_id to the ID of the email or group from whom you are revoking access.
    entity_id = "user-or-group-to-remove@example.com"
    # [END bigquery_revoke_dataset_access]
    dataset_id = original_dataset_id
    entity_id = original_entity_id
    # [START bigquery_revoke_dataset_access]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    dataset = client.get_dataset(dataset_id)  # Make an API request.

    entries = list(dataset.access_entries)
    dataset.access_entries = [
        entry for entry in entries if entry.entity_id != entity_id
    ]

    dataset = client.update_dataset(
        dataset,
        # Update just the `access_entries` property of the dataset.
        ["access_entries"],
    )  # Make an API request.

    full_dataset_id = f"{dataset.project}.{dataset.dataset_id}"
    print(f"Revoked dataset access for '{entity_id}' to ' dataset '{full_dataset_id}.'")
    # [END bigquery_revoke_dataset_access]
