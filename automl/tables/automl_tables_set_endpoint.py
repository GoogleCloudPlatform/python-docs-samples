# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def create_client_with_endpoint(gcp_project_id):
    """Create a Tables client with a non-default endpoint."""
    # [START automl_set_endpoint]
    from google.cloud import automl_v1beta1 as automl
    from google.api_core.client_options import ClientOptions

    # Set the endpoint you want to use via the ClientOptions.
    # gcp_project_id = 'YOUR_PROJECT_ID'
    client_options = ClientOptions(api_endpoint="eu-automl.googleapis.com:443")
    client = automl.TablesClient(
        project=gcp_project_id, region="eu", client_options=client_options
    )
    # [END automl_set_endpoint]

    # do simple test to check client connectivity
    print(client.list_datasets())

    return client
