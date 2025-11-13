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

# [START auth_custom_credential_supplier_okta]
import json
import os
import sys
import time
import urllib.parse

import requests
from google.auth import identity_pool
from google.auth.transport import requests as auth_requests

class OktaClientCredentialsSupplier:
    """A custom SubjectTokenSupplier that authenticates with Okta.

    This supplier uses the Client Credentials grant flow for machine-to-machine
    (M2M) authentication with Okta.
    """

    def __init__(self, domain, client_id, client_secret):
        self.okta_token_url = f"{domain.rstrip('/')}/oauth2/default/v1/token"
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.expiry_time = 0

    def get_subject_token(self, context, request=None) -> str:
        """Fetches a new token if the current one is expired or missing."""
        # Check if the current token is still valid (with a 60-second buffer).
        if self.access_token and time.time() < self.expiry_time - 60:
            return self.access_token

        print("[Supplier] Fetching new Okta Access token...")
        self._fetch_okta_access_token()
        return self.access_token

    def _fetch_okta_access_token(self):
        """Performs the Client Credentials grant flow with Okta."""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            "grant_type": "client_credentials",
            "scope": "gcp.test.read", # Set scope as per Okta app config.
        }

        response = requests.post(
            self.okta_token_url,
            headers=headers,
            data=urllib.parse.urlencode(data),
            auth=(self.client_id, self.client_secret),
        )
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.expiry_time = time.time() + token_data["expires_in"]


def authenticate_with_okta_credentials(
    bucket_name, audience, domain, client_id, client_secret, impersonation_url
):
    """Authenticates using the custom Okta supplier and lists bucket metadata."""
    
    # 1. Instantiate the custom supplier.
    okta_supplier = OktaClientCredentialsSupplier(domain, client_id, client_secret)

    # 2. Instantiate the IdentityPoolClient.
    # This client exchanges the Okta token for a Google Federated Token.
    client = identity_pool.Credentials(
        audience=audience,
        subject_token_type="urn:ietf:params:oauth:token-type:jwt",
        token_url="https://sts.googleapis.com/v1/token",
        subject_token_supplier=okta_supplier,
        default_scopes=["https://www.googleapis.com/auth/devstorage.read_write"],
        service_account_impersonation_url=impersonation_url,
    )

    # 3. Create an authenticated session.
    authed_session = auth_requests.AuthorizedSession(client)

    # 4. Make the API Request.
    bucket_url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}"
    print(f"Request URL: {bucket_url}")
    
    response = authed_session.get(bucket_url)
    response.raise_for_status()

    print("\n--- SUCCESS! ---")
    print(json.dumps(response.json(), indent=2))

# [END auth_custom_credential_supplier_okta]

from dotenv import load_dotenv

def main():
    load_dotenv()
    
    # Configuration
    gcp_audience = os.getenv("GCP_WORKLOAD_AUDIENCE")
    gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
    # Optional: Service Account Impersonation
    sa_impersonation_url = os.getenv("GCP_SERVICE_ACCOUNT_IMPERSONATION_URL")

    okta_domain = os.getenv("OKTA_DOMAIN")
    okta_client_id = os.getenv("OKTA_CLIENT_ID")
    okta_client_secret = os.getenv("OKTA_CLIENT_SECRET")

    if not all([gcp_audience, gcs_bucket_name, okta_domain, okta_client_id, okta_client_secret]):
        print("[ERROR] Missing required environment variables.", file=sys.stderr)
        sys.exit(1)

    try:
        authenticate_with_okta_credentials(
            bucket_name=gcs_bucket_name,
            audience=gcp_audience,
            domain=okta_domain,
            client_id=okta_client_id,
            client_secret=okta_client_secret,
            impersonation_url=sa_impersonation_url,
        )
    except Exception as e:
        print(f"[ERROR] Authentication or Request failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()