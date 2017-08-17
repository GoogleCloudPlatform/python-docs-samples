# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example use of a service account with user-managed keys
   to authenticate to Identity-Aware Proxy."""

# [START iap_make_request_external]
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import requests
import json


def make_iap_request(url, client_id, json_private_key):
    """Makes a request to an application protected by Identity-Aware Proxy.

      Args:
        url: The Identity-Aware Proxy-protected URL to fetch.
        client_id: The client ID used by Identity-Aware Proxy.
        json_private_key: Path to the json private key file

      Returns:
        The page body, or raises an exception if the page couldn't be retrieved.
      """
    # Construct OAuth 2.0 service account credentials using the
    # service account's associated json private key file
    service_account_credentials = get_service_account_credentials(
      client_id, json_private_key)

    # service_account_credentials gives us a JWT signed by the service
    # account. Next, we use that to obtain an OpenID Connect token,
    # which is a JWT signed by Google.
    google_open_id_connect_token = get_google_open_id_connect_token(
      service_account_credentials)

    # Fetch the Identity-Aware Proxy-protected URL, including an
    # Authorization header containing "Bearer " followed by a
    # Google-issued OpenID Connect token for the service account.
    resp = requests.get(
        url,
        headers={'Authorization': 'Bearer {}'.format(
            google_open_id_connect_token)},
        # Do not set verify=False in production!!
        # This is only for sample using self-signed certs
        verify=False)
    return resp.text

def get_service_account_credentials(iap_client_id, json_private_key):
    """Create Service Account credential from downloaded JSON private key file.

    Args:
      iap_client_id: The client ID used by Identity-Aware Proxy.
      json_private_key: The json private key file for the service account

    Returns:
      OAuth 2.0 signed JWT-based access token (JWT-bAT)
    """
    # Create Service Account credential from downloaded JSON private key file.
    # Note: Additional claim of 'target_audience' is required and must be
    # set to the clientId of the IAP Service Account
    credentials = Credentials.from_service_account_file(json_private_key
                 ).with_claims({'target_audience': iap_client_id})
    # Must change credential's token uri to point to Google's
    # OpenId token endpoint instead of Google's authorization endpoint
    credentials._token_uri = get_token_endpoint()
    # Generate and return OAuth 2.0 signed JWT-based access token (JWT-bAT)
    return credentials

def get_google_open_id_connect_token(service_account_credentials):
    """Get an OpenID Connect token issued by Google for the service account.

    This function:

      1. Generates a JWT signed with the service account's private key
         containing a special "target_audience" claim.

      2. Sends it to the oauth token uri endpoint. Because the JWT in #1
         has a target_audience claim, that endpoint will respond with
         an OpenID Connect token for the service account -- in other words,
         a JWT signed by *Google*. The aud claim in this JWT will be
         set to the value from the target_audience claim in #1.

    For more information, see
    https://developers.google.com/identity/protocols/OAuth2ServiceAccount .
    The HTTP/REST example on that page describes the JWT structure and
    demonstrates how to call the token endpoint. (The example on that page
    shows how to get an OAuth2 access token; this code is using a
    modified version of it to get an OpenID Connect token.)
    """
    service_account_jwt = (
      service_account_credentials._make_authorization_grant_assertion())
    # Request OpenID Connect (OIDC) token for Cloud IAP-secured client ID.
    request = google.auth.transport.requests.Request()
    body = {
        'assertion': service_account_jwt,
        'grant_type': google.oauth2._client._JWT_GRANT_TYPE,
    }
    token_response = google.oauth2._client._token_endpoint_request(
        request, get_token_endpoint(), body)
    return token_response['id_token']

def get_token_endpoint():
    """Makes a request to Google's openid endpoint and returns
    the oauth token uri. This function eliminates the need to
    hardcode the oauth token uri which is subject to future changes.
    """
    response = requests.get(
      "https://accounts.google.com/.well-known/openid-configuration")
    return json.loads(response.text)["token_endpoint"]

# [END iap_make_request_external]
