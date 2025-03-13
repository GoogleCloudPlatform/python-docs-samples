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

from google.cloud.bigquery.dataset import AccessEntry


def revoke_dataset_access(dataset_id: str, entity_id: str) -> list[AccessEntry]:
    # [START bigquery_revoke_dataset_access]
    from google.cloud import bigquery
    from google.api_core.exceptions import PreconditionFailed

    # TODO(developer): Update and uncomment the lines below.

    # ID of the dataset to revoke access to.
    # dataset_id = "my-project.my_dataset"

    # ID of the user or group from whom you are revoking access.
    # Alternatively, the JSON REST API representation of the entity,
    # such as a view's table reference.
    # entity_id = "user-or-group-to-remove@example.com"

    # Instantiate a client.
    client = bigquery.Client()

    # Get a reference to the dataset.
    dataset = client.get_dataset(dataset_id)

    # To revoke access to a dataset, remove elements from the AccessEntry list.
    #
    # See the BigQuery client library documentation for more details on `access_entries`:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.Dataset#google_cloud_bigquery_dataset_Dataset_access_entries

    # Filter `access_entries` to exclude entries matching the specified entity_id
    # and assign a new list back to the AccessEntry list.
    dataset.access_entries = [
        entry for entry in dataset.access_entries
        if entry.entity_id != entity_id
    ]

    # Update will only succeed if the dataset
    # has not been modified externally since retrieval.
    #
    # See the BigQuery client library documentation for more details on `update_dataset`:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_update_dataset
    try:
        # Update just the `access_entries` property of the dataset.
        dataset = client.update_dataset(
            dataset,
            ["access_entries"],
        )

        # Notify user that the API call was successful.
        full_dataset_id = f"{dataset.project}.{dataset.dataset_id}"
        print(f"Revoked dataset access for '{entity_id}' to ' dataset '{full_dataset_id}.'")
    except PreconditionFailed:  # A read-modify-write error.
        print(
            f"Dataset '{dataset.dataset_id}' was modified remotely before this update. "
            "Fetch the latest version and retry."
        )
    # [END bigquery_revoke_dataset_access]

    return dataset.access_entries
