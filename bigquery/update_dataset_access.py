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


def update_dataset_access(dataset_id):

    # [START bigquery_update_dataset_access]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    # dataset_id = 'your-project.your_dataset'

    dataset = client.get_dataset(dataset_id)  # Make an API request.

    entry = bigquery.AccessEntry(
        role="READER",
        entity_type="groupByEmail",
        entity_id="cloud-developer-relations@google.com",
    )

    entries = list(dataset.access_entries)
    entries.append(entry)
    dataset.access_entries = entries

    dataset = client.update_dataset(dataset, ["access_entries"])  # Make an API request.

    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    print(
        "Updated dataset '{}' with modified user permissions.".format(full_dataset_id)
    )
    # [END bigquery_update_dataset_access]
