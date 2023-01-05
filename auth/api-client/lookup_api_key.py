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

# [START apikeys_lookup_api_key]

from google.cloud import api_keys_v2


def lookup_api_key(api_key_string: str) -> None:
    """
    Retrieves name (full path) of an API key using the API key string.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to view API keys.

    Args:
        api_key_string: API key string to retrieve the API key name.
    """

    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    # Initialize the lookup request and set the API key string.
    lookup_key_request = api_keys_v2.LookupKeyRequest(
      key_string=api_key_string,
      # Optionally, you can also set the etag (version).
      # etag=etag,
    )

    # Make the request and obtain the response.
    lookup_key_response = client.lookup_key(lookup_key_request)

    print(f"Successfully retrieved the API key name: {lookup_key_response.name}")

# [END apikeys_lookup_api_key]
