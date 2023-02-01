# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START apikeys_delete_api_key]

from google.cloud import api_keys_v2


def delete_api_key(project_id: str, key_id: str) -> None:
    """
    Deletes an API key.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to delete API keys.

    Args:
        project_id: Google Cloud project id that has the API key to delete.
        key_id: The API key id to delete.
    """

    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    # Initialize the delete request and set the argument.
    delete_key_request = api_keys_v2.DeleteKeyRequest()
    delete_key_request.name = f"projects/{project_id}/locations/global/keys/{key_id}"

    # Make the request and wait for the operation to complete.
    result = client.delete_key(delete_key_request).result()
    print(f"Successfully deleted the API key: {result.name}")

# [END apikeys_delete_api_key]
