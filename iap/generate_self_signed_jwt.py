# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import time

import google.auth
from google.cloud import iam_credentials_v1
import jwt

# [START iap_generate_self_signed_jwt]


def generate_jwt_payload(service_account_email: str, resource_url: str) -> str:
    """Generates JWT payload for service account.

    The resource url provided must be the same as the url of the IAP secured resource.

    Args:
      service_account_email (str): Specifies service account JWT is created for.
      resource_url (str): Specifies scope of the JWT, the URL that the JWT will be allowed to access.
    Returns:
      A signed-jwt that can be used to access IAP protected applications.
      Access the application with the JWT in the Authorization Header.
      curl --verbose --header 'Authorization: Bearer SIGNED_JWT' URL
    """
    now = int(time.time())

    return json.dumps(
        {
            "iss": service_account_email,
            "sub": service_account_email,
            "aud": resource_url,
            "iat": now,
            "exp": now + 3600,
        }
    )


# [END iap_generate_self_signed_jwt]
# [START iap_sign_jwt_IAM]


def sign_jwt(target_sa: str, resource_url: str) -> str:
    """Signs JWT payload using ADC and IAM credentials API.

    Args:
      target_sa (str): Service Account JWT is being created for.
        iap.webServiceVersions.accessViaIap permission is required.
      resource_url (str): Audience of the JWT, and scope of the JWT token.
        This is the url of the IAP protected application.
    Returns:
      A signed-jwt that can be used to access IAP protected apps.
    """
    source_credentials, _ = google.auth.default()
    iam_client = iam_credentials_v1.IAMCredentialsClient(credentials=source_credentials)
    return iam_client.sign_jwt(
        name=iam_client.service_account_path("-", target_sa),
        payload=generate_jwt_payload(target_sa, resource_url),
    ).signed_jwt


# [END iap_sign_jwt_IAM]
# [START iap_sign_jwt_with_key_file]


def sign_jwt_with_key_file(credential_key_file_path: str, resource_url: str) -> str:
    """Signs JWT payload using local service account credential key file.

    Args:
      credential_key_file_path (str): Path to the downloaded JSON credentials of the service
        account the JWT is being created for.
      resource_url (str): Scope of JWT token, This is the url of the IAP protected application.
    Returns:
      A self-signed JWT created with a downloaded private key.
    """
    with open(credential_key_file_path, "r") as credential_key_file:
        key_data = json.load(credential_key_file)

    PRIVATE_KEY_ID_FROM_JSON = key_data["private_key_id"]
    PRIVATE_KEY_FROM_JSON = key_data["private_key"]
    SERVICE_ACCOUNT_EMAIL = key_data["client_email"]

    # Sign JWT with private key and store key id in the header
    additional_headers = {"kid": PRIVATE_KEY_ID_FROM_JSON}
    payload = generate_jwt_payload(
        service_account_email=SERVICE_ACCOUNT_EMAIL, resource_url=resource_url
    )

    signed_jwt = jwt.encode(
        payload,
        PRIVATE_KEY_FROM_JSON,
        headers=additional_headers,
        algorithm="RS256",
    )
    return signed_jwt


# [END iap_sign_jwt_with_key_file]

# sign_jwt("test_email", "resource-url")
# sign_jwt_with_key_file("/path/to/local/key/file.json", "resource-url")
