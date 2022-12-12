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


def set_endpoint(project_id):
    """Change your endpoint"""
    # [START automl_set_endpoint]
    from google.cloud import automl_v1beta1 as automl

    # You must first create a dataset, using the `eu` endpoint, before you can
    # call other operations such as: list, get, import, delete, etc.
    client_options = {'api_endpoint': 'eu-automl.googleapis.com:443'}

    # Instantiates a client
    client = automl.AutoMlClient(client_options=client_options)

    # A resource that represents Google Cloud Platform location.
    # project_id = 'YOUR_PROJECT_ID'
    project_location = f"projects/{project_id}/locations/eu"
    # [END automl_set_endpoint]

    # List all the datasets available
    # Note: Create a dataset in `eu`, before calling `list_datasets`.
    request = automl.ListDatasetsRequest(
        parent=project_location,
        filter=""
    )
    response = client.list_datasets(
        request=request
    )

    for dataset in response:
        print(dataset)
