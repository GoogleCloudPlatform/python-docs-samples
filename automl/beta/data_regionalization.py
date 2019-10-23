# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def data_regionalization(project_id):
    """Set a regional data endpoint using data regionalization"""
    # [START automl_client_library]
    # [START automl_data_regionalization]
    from google.cloud import automl_v1beta1 as automl

    client_options = {'api_endpoint': 'eu-automl.googleapis.com:443'}

    # Instantiates a client
    client = automl.AutoMlClient(client_options=client_options)
    # [END automl_data_regionalization]

    # A resource that represents Google Cloud Platform location.
    # project_id = 'YOUR_PROJECT_ID'
    project_location = client.location_path(project_id, 'eu')

    # List all the datasets available in the region.
    response = client.list_datasets(
        project_location, 'translation_dataset_metadata:*')

    for dataset in response:
        print(dataset)
    # [END automl_client_library]
