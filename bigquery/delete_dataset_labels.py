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


def delete_dataset_labels(client, dataset_id):

    # [START bigquery_delete_label_dataset]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    # dataset_id = "your-project.your_dataset"

    dataset = client.get_dataset(dataset_id)

    # To delete a label from a dataset, set its value to None
    dataset.labels["color"] = None

    dataset = client.update_dataset(dataset, ["labels"])
    print("Labels deleted from {}".format(dataset_id))
    # [END bigquery_delete_label_dataset]
    return dataset
