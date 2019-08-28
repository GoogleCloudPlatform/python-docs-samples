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


def update_dataset_default_table_expiration(client, dataset_id):

    # [START bigquery_update_dataset_expiration]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    # dataset_id = 'your-project.your_dataset'

    dataset = client.get_dataset(dataset_id)
    dataset.default_table_expiration_ms = 24 * 60 * 60 * 1000  # in milliseconds

    dataset = client.update_dataset(
        dataset, ["default_table_expiration_ms"]
    )  # API request

    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    print(
        "Updated dataset {} with new expiration {}".format(
            full_dataset_id, dataset.default_table_expiration_ms
        )
    )
    # [END bigquery_update_dataset_expiration]
