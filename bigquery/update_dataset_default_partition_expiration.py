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


def update_dataset_default_partition_expiration(dataset_id: str) -> None:
    # [START bigquery_update_dataset_partition_expiration]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    # dataset_id = 'your-project.your_dataset'

    dataset = client.get_dataset(dataset_id)  # Make an API request.

    # Set the default partition expiration (applies to new tables, only) in
    # milliseconds. This example sets the default expiration to 90 days.
    dataset.default_partition_expiration_ms = 90 * 24 * 60 * 60 * 1000

    dataset = client.update_dataset(
        dataset, ["default_partition_expiration_ms"]
    )  # Make an API request.

    print(
        "Updated dataset {}.{} with new default partition expiration {}".format(
            dataset.project, dataset.dataset_id, dataset.default_partition_expiration_ms
        )
    )
    # [END bigquery_update_dataset_partition_expiration]
