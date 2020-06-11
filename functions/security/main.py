# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_bearer_token]
import requests

# TODO<developer>: set these values
REGION = 'us-central1'
PROJECT_ID = 'my-project'
RECEIVING_FUNCTION = 'my-function'

# Constants for setting up metadata server request
# See https://cloud.google.com/compute/docs/instances/verifying-instance-identity#request_signature
function_url = f'https://{REGION}-{PROJECT_ID}.cloudfunctions.net/{RECEIVING_FUNCTION}'
metadata_server_url = \
    'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='
token_full_url = metadata_server_url + function_url
token_headers = {'Metadata-Flavor': 'Google'}


def calling_function(request):
    # Fetch the token
    token_response = requests.get(token_full_url, headers=token_headers)
    jwt = token_response.text

    # Provide the token in the request to the receiving function
    function_headers = {'Authorization': f'bearer {jwt}'}
    function_response = requests.get(function_url, headers=function_headers)

    return function_response.text
# [END functions_bearer_token]
