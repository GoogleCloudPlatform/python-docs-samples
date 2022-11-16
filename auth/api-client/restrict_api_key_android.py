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

# [START auth_cloud_restrict_api_key_android]

from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def restrict_api_key_android(project_id: str, key_id: str) -> Key:
    """
    Restricts an API key based on android applications.

    Specifies the Android application that can use the key.

    TODO(Developer): Replace the variables before running this sample.

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

    # Specify the android application's package name and SHA1 fingerprint.
    allowed_application = api_keys_v2.AndroidApplication()
    allowed_application.package_name = "com.google.appname"
    allowed_application.sha1_fingerprint = "0873D391E987982FBBD30873D391E987982FBBD3"

    # Restrict the API key usage by specifying the allowed applications.
    android_key_restriction = api_keys_v2.AndroidKeyRestrictions()
    android_key_restriction.allowed_applications = [allowed_application]

    # Set the restriction(s).
    # For more information on API key restriction, see:
    # https://cloud.google.com/docs/authentication/api-keys
    restrictions = api_keys_v2.Restrictions()
    restrictions.android_key_restrictions = android_key_restriction

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

# [END auth_cloud_restrict_api_key_android]
