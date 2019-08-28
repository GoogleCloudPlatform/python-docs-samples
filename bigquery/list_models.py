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


def list_models(client, dataset_id):
    """Sample ID: go/samples-tracker/1512"""

    # [START bigquery_list_models]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset that contains
    #                  the models you are listing.
    # dataset_id = 'your-project.your_dataset'

    models = client.list_models(dataset_id)

    print("Models contained in '{}':".format(dataset_id))
    for model in models:
        full_model_id = "{}.{}.{}".format(
            model.project, model.dataset_id, model.model_id
        )
        friendly_name = model.friendly_name
        print("{}: friendly_name='{}'".format(full_model_id, friendly_name))
    # [END bigquery_list_models]
