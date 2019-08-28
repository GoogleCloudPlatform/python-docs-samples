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


def delete_dataset(client, dataset_id):

    # [START bigquery_delete_dataset]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set model_id to the ID of the model to fetch.
    # dataset_id = 'your-project.your_dataset'

    # Use the delete_contents parameter to delete a dataset and its contents
    # Use the not_found_ok parameter to not receive an error if the dataset has already been deleted.
    client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)

    print("Deleted dataset '{}'.".format(dataset_id))
    # [END bigquery_delete_dataset]
