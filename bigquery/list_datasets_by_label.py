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


def list_datasets_by_label() -> None:
    # [START bigquery_list_datasets_by_label]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    label_filter = "labels.color:green"
    datasets = list(client.list_datasets(filter=label_filter))  # Make an API request.

    if datasets:
        print("Datasets filtered by {}:".format(label_filter))
        for dataset in datasets:
            print("\t{}.{}".format(dataset.project, dataset.dataset_id))
    else:
        print("No datasets found with this filter.")
    # [END bigquery_list_datasets_by_label]
