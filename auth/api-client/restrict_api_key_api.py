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

# [START apikeys_restrict_api_key_api]

from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def restrict_api_key_api(project_id: str, key_id: str) -> Key:
    """
    Restricts an API key. Restrictions specify which APIs can be called using the API key.

    TODO(Developer): Replace the variables before running the sample.

    Args:
        project_id: Google Cloud project id.
        key_id: ID of the key to restrict. This ID is auto-created during key creation.
            This is different from the key string. To obtain the key_id,
            you can also use the lookup api: client.lookup_key()

    Returns:
        response: Returns the updated API Key.
    """

    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    # Restrict the API key usage by specifying the target service and methods.
    # The API key can only be used to authenticate the specified methods in the service.
    api_target = api_keys_v2.ApiTarget()
    api_target.service = "translate.googleapis.com"
    api_target.methods = ["transate.googleapis.com.TranslateText"]

    # Set the API restriction(s).
    # For more information on API key restriction, see:
    # https://cloud.google.com/docs/authentication/api-keys
    restrictions = api_keys_v2.Restrictions()
    restrictions.api_targets = [api_target]

    key = api_keys_v2.Key()
    key.name = f"projects/{project_id}/locations/global/keys/{key_id}"
    key.restrictions = restrictions

    # Initialize request and set arguments.
    request = api_keys_v2.UpdateKeyRequest()
    request.key = key
    request.update_mask = "restrictions"

    # Make the request and wait for the operation to complete.
    response = client.update_key(request=request).result()

    print(f"Successfully updated the API key: {response.name}")
    # Use response.key_string to authenticate.
    return response

# [END apikeys_restrict_api_key_api]
