# Copyright 2019 Google LLC
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


def update_dataset_access(dataset_id: str, entity_id: str):
    original_dataset_id = dataset_id
    original_entity_id = entity_id

    # [START bigquery_update_dataset_access]

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    dataset_id = "your-project.your_dataset"

    # TODO(developer): Set entity_id to the ID of the email or group from whom
    # you are adding access. Alternatively, to the JSON REST API representation
    # of the entity, such as a view's table reference.
    entity_id = "user-or-group-to-add@example.com"

    from google.cloud.bigquery.enums import EntityTypes

    # TODO(developer): Set entity_type to the type of entity you are granting access to.
    # Common types include:
    #
    # * "userByEmail" -- A single user or service account. For example "fred@example.com"
    # * "groupByEmail" -- A group of users. For example "example@googlegroups.com"
    # * "view" -- An authorized view. For example
    #       {"projectId": "p", "datasetId": "d", "tableId": "v"}
    #
    # For a complete reference, see the REST API reference documentation:
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#Dataset.FIELDS.access
    entity_type = EntityTypes.GROUP_BY_EMAIL

    # TODO(developer): Set role to a one of the "Basic roles for datasets"
    # described here:
    # https://cloud.google.com/bigquery/docs/access-control-basic-roles#dataset-basic-roles
    role = "READER"
    # [END bigquery_update_dataset_access]
    dataset_id = original_dataset_id
    entity_id = original_entity_id
    # [START bigquery_update_dataset_access]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    dataset = client.get_dataset(dataset_id)  # Make an API request.

    entries = list(dataset.access_entries)
    entries.append(
        bigquery.AccessEntry(
            role=role,
            entity_type=entity_type,
            entity_id=entity_id,
        )
    )
    dataset.access_entries = entries

    dataset = client.update_dataset(dataset, ["access_entries"])  # Make an API request.

    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    print(
        "Updated dataset '{}' with modified user permissions.".format(full_dataset_id)
    )
    # [END bigquery_update_dataset_access]
