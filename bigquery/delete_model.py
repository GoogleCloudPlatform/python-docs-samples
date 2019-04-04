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


def delete_model(client, model_id):
    """Sample ID: go/samples-tracker/1534"""

    # [START bigquery_delete_model]
    from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set model_id to the ID of the model to fetch.
    # model_id = 'your-project.your_dataset.your_model'

    client.delete_model(model_id)
    # [END bigquery_delete_model]

    print("Deleted model '{}'.".format(model_id))
