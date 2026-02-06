# Copyright 2025 Google LLC
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

import json
import os
import time
import urllib.parse

from dotenv import load_dotenv
import requests

from google.auth.exceptions import GoogleAuthError
from google.auth.identity_pool import Credentials as IdentityPoolClient
from google.auth.transport.requests import AuthorizedSession

load_dotenv()

# Workload Identity Pool Configuration
GCP_WORKLOAD_AUDIENCE = os.getenv("GCP_WORKLOAD_AUDIENCE")
SERVICE_ACCOUNT_IMPERSONATION_URL = os.getenv("GCP_SERVICE_ACCOUNT_IMPERSONATION_URL")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

# Okta Configuration
OKTA_DOMAIN = os.getenv("OKTA_DOMAIN")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")

# Constants
TOKEN_URL = "https://sts.googleapis.com/v1/token"
SUBJECT_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:jwt"


class OktaClientCredentialsSupplier:
    """A custom SubjectTokenSupplier that authenticates with Okta.

    This supplier uses the Client Credentials grant flow for machine-to-machine
    (M2M) authentication with Okta.
    """

    def __init__(self, domain: str, client_id: str, client_secret: str) -> None:
        self.okta_token_url = f"{domain}/oauth2/default/v1/token"
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.expiry_time = 0
        print("OktaClientCredentialsSupplier initialized.")

    def get_subject_token(self, context: object, request: object = None) -> str:
        """Fetches a new token if the current one is expired or missing.

        Args:
            context: The context object, not used in this implementation.

        Returns:
            The Okta Access token.
        """
        # Check if the current token is still valid (with a 60-second buffer).
        is_token_valid = self.access_token and time.time() < self.expiry_time - 60

        if is_token_valid:
            print("[Supplier] Returning cached Okta Access token.")
            return self.access_token

        print(
            "[Supplier] Token is missing or expired. Fetching new Okta Access token..."
        )
        self._fetch_okta_access_token()
        return self.access_token

    def _fetch_okta_access_token(self) -> None:
        """Performs the Client Credentials grant flow with Okta."""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            "grant_type": "client_credentials",
            "scope": "gcp.test.read",
        }
        encoded_data = urllib.parse.urlencode(data)

        try:
            response = requests.post(
                self.okta_token_url,
                headers=headers,
                data=encoded_data,
                auth=(self.client_id, self.client_secret),
            )
            response.raise_for_status()
            token_data = response.json()

            if "access_token" in token_data and "expires_in" in token_data:
                self.access_token = token_data["access_token"]
                self.expiry_time = time.time() + token_data["expires_in"]
                print(
                    f"[Supplier] Successfully received Access Token from Okta. "
                    f"Expires in {token_data['expires_in']} seconds."
                )
            else:
                raise GoogleAuthError(
                    "Access token or expires_in not found in Okta response."
                )
        except requests.exceptions.RequestException as e:
            print(f"[Supplier] Error fetching token from Okta: {e}")
            if e.response:
                print(f"[Supplier] Okta response: {e.response.text}")
            raise GoogleAuthError(
                "Failed to authenticate with Okta using Client Credentials grant."
            ) from e


def main() -> None:
    """Main function to demonstrate the custom Okta supplier.

    TODO(Developer):
    1. Before running this sample, set up your environment variables. You can do
       this by creating a .env file in the same directory as this script and
       populating it with the following variables:
       - GCP_WORKLOAD_AUDIENCE: The audience for the GCP workload identity pool.
       - GCP_SERVICE_ACCOUNT_IMPERSONATION_URL: The URL for service account impersonation (optional).
       - GCS_BUCKET_NAME: The name of the GCS bucket to access.
       - OKTA_DOMAIN: Your Okta domain (e.g., https://dev-12345.okta.com).
       - OKTA_CLIENT_ID: The Client ID of your Okta M2M application.
       - OKTA_CLIENT_SECRET: The Client Secret of your Okta M2M application.
    """
    if not all(
        [
            GCP_WORKLOAD_AUDIENCE,
            GCS_BUCKET_NAME,
            OKTA_DOMAIN,
            OKTA_CLIENT_ID,
            OKTA_CLIENT_SECRET,
        ]
    ):
        raise GoogleAuthError(
            "Missing required environment variables. Please check your .env file."
        )

    # 1. Instantiate the custom supplier with Okta credentials.
    okta_supplier = OktaClientCredentialsSupplier(
        OKTA_DOMAIN, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET
    )

    # 2. Instantiate an IdentityPoolClient.
    client = IdentityPoolClient(
        audience=GCP_WORKLOAD_AUDIENCE,
        subject_token_type=SUBJECT_TOKEN_TYPE,
        token_url=TOKEN_URL,
        subject_token_supplier=okta_supplier,
        # If you choose to provide explicit scopes: use the `scopes` parameter.
        default_scopes=['https://www.googleapis.com/auth/cloud-platform'],
        service_account_impersonation_url=SERVICE_ACCOUNT_IMPERSONATION_URL,
    )

    # 3. Construct the URL for the Cloud Storage JSON API.
    bucket_url = f"https://storage.googleapis.com/storage/v1/b/{GCS_BUCKET_NAME}"
    print(f"[Test] Getting metadata for bucket: {GCS_BUCKET_NAME}...")
    print(f"[Test] Request URL: {bucket_url}")

    # 4. Use the client to make an authenticated request.
    authed_session = AuthorizedSession(client)
    try:
        res = authed_session.get(bucket_url)
        res.raise_for_status()
        print("\n--- SUCCESS! ---")
        print("Successfully authenticated and retrieved bucket data:")
        print(json.dumps(res.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print("\n--- FAILED ---")
        print(f"Request failed: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        exit(1)
    except GoogleAuthError as e:
        print("\n--- FAILED ---")
        print(f"Authentication or request failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
