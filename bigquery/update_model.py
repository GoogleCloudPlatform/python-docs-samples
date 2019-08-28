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


def update_model(client, model_id):
    """Sample ID: go/samples-tracker/1533"""

    # [START bigquery_update_model_description]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set model_id to the ID of the model to fetch.
    # model_id = 'your-project.your_dataset.your_model'

    model = client.get_model(model_id)
    model.description = "This model was modified from a Python program."
    model = client.update_model(model, ["description"])

    full_model_id = "{}.{}.{}".format(model.project, model.dataset_id, model.model_id)
    print(
        "Updated model '{}' with description '{}'.".format(
            full_model_id, model.description
        )
    )
    # [END bigquery_update_model_description]
