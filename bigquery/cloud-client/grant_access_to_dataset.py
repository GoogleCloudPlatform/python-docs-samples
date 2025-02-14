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
    user_email: str,
    role: str
) -> list[AccessEntry]:
    # [START bigquery_grant_access_to_dataset]
    from google.cloud import bigquery
    from google.cloud.bigquery.enums import EntityTypes

    # TODO(developer): Update and un-comment below lines
    # ID of the dataset to fetch.
    # dataset_id = "my_project_id.my_dataset"

    # ID of the email or group from whom you are adding access.
    # Alternatively, the JSON REST API representation of the entity,
    # such as a view's table reference.
    # user_email = "user-or-group-to-add@example.com"

    # One of the "Basic roles for datasets" described here:
    # https://cloud.google.com/bigquery/docs/access-control-basic-roles#dataset-basic-roles
    # role = "READER"

    # Type of entity you are granting access to.
    # https://cloud.google.com/python/docs/reference/bigquery/latest/enums#class-googlecloudbigqueryenumsentitytypesvalue
    #
    # For a complete reference, see the REST API reference documentation:
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#Dataset.FIELDS.access
    entity_type = EntityTypes.USER_BY_EMAIL

    # Instantiate a client.
    client = bigquery.Client()

    # Prepare a reference to the dataset.
    dataset = client.get_dataset(dataset_id)

    # Copy the list of access_entries in order to add new roles.
    # Don't try to append AccessEntries directly
    # to dataset.access_entries as it won't work.
    entries = list(dataset.access_entries)

    # Add an AccessEntry to grant the role to a dataset.
    # Find more details about the AccessEntry object here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry
    entries.append(
        bigquery.AccessEntry(
            role=role,
            entity_type=entity_type,
            entity_id=user_email,
        )
    )

    # Assign the list of AccessEntries back to the dataset and update it.
    dataset.access_entries = entries
    dataset = client.update_dataset(dataset, ["access_entries"])

    # Show a success message.
    full_dataset_id = f"{dataset.project}.{dataset.dataset_id}"
    print(
        f"Role '{role}' granted for user '{user_email}'"
        f" in dataset '{full_dataset_id}'."
    )
    # [END bigquery_grant_access_to_dataset]

    return dataset.access_entries
