# Copyright 2025 Google LLC
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


def grant_access_to_dataset(
    dataset_id: str,
    entity_id: str,
    role: str
) -> list[AccessEntry]:
    # [START bigquery_grant_access_to_dataset]
    from google.api_core.exceptions import PreconditionFailed
    from google.cloud import bigquery
    from google.cloud.bigquery.enums import EntityTypes

    # TODO(developer): Update and uncomment the lines below.

    # ID of the dataset to grant access to.
    # dataset_id = "my_project_id.my_dataset"

    # ID of the user or group receiving access to the dataset.
    # Alternatively, the JSON REST API representation of the entity,
    # such as the view's table reference.
    # entity_id = "user-or-group-to-add@example.com"

    # One of the "Basic roles for datasets" described here:
    # https://cloud.google.com/bigquery/docs/access-control-basic-roles#dataset-basic-roles
    # role = "READER"

    # Type of entity you are granting access to.
    # Find allowed allowed entity type names here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/enums#class-googlecloudbigqueryenumsentitytypesvalue
    entity_type = EntityTypes.GROUP_BY_EMAIL

    # Instantiate a client.
    client = bigquery.Client()

    # Get a reference to the dataset.
    dataset = client.get_dataset(dataset_id)

    # The `access_entries` list is immutable. Create a copy for modifications.
    entries = list(dataset.access_entries)

    # Append an AccessEntry to grant the role to a dataset.
    # Find more details about the AccessEntry object here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry
    entries.append(
        bigquery.AccessEntry(
            role=role,
            entity_type=entity_type,
            entity_id=entity_id,
        )
    )

    # Assign the list of AccessEntries back to the dataset.
    dataset.access_entries = entries

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

        # Show a success message.
        full_dataset_id = f"{dataset.project}.{dataset.dataset_id}"
        print(
            f"Role '{role}' granted for entity '{entity_id}'"
            f" in dataset '{full_dataset_id}'."
        )
    except PreconditionFailed:  # A read-modify-write error
        print(
            f"Dataset '{dataset.dataset_id}' was modified remotely before this update. "
            "Fetch the latest version and retry."
        )
    # [END bigquery_grant_access_to_dataset]

    return dataset.access_entries
