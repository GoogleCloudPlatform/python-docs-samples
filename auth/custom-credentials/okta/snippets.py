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
import time
import urllib.parse

from google.auth import identity_pool
from google.cloud import storage
import requests


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
        if self.access_token and time.time() < self.expiry_time - 60:
            return self.access_token
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
            "scope": "gcp.test.read",  # Set scope as per Okta app config.
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
    bucket_name, audience, domain, client_id, client_secret, impersonation_url=None
):
    """Authenticates using the custom Okta supplier and gets bucket metadata.

    Returns:
        dict: The bucket metadata response from the Google Cloud Storage API.
    """

    okta_supplier = OktaClientCredentialsSupplier(domain, client_id, client_secret)

    credentials = identity_pool.Credentials(
        audience=audience,
        subject_token_type="urn:ietf:params:oauth:token-type:jwt",
        token_url="https://sts.googleapis.com/v1/token",
        subject_token_supplier=okta_supplier,
        default_scopes=["https://www.googleapis.com/auth/devstorage.read_only"],
        service_account_impersonation_url=impersonation_url,
    )

    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.get_bucket(bucket_name)

    return bucket._properties


# [END auth_custom_credential_supplier_okta]


def main():
    try:
        with open("custom-credentials-okta-secrets.json") as f:
            secrets = json.load(f)
    except FileNotFoundError:
        print("Could not find custom-credentials-okta-secrets.json.")
        return

    gcp_audience = secrets.get("gcp_workload_audience")
    gcs_bucket_name = secrets.get("gcs_bucket_name")
    sa_impersonation_url = secrets.get("gcp_service_account_impersonation_url")

    okta_domain = secrets.get("okta_domain")
    okta_client_id = secrets.get("okta_client_id")
    okta_client_secret = secrets.get("okta_client_secret")

    if not all(
        [gcp_audience, gcs_bucket_name, okta_domain, okta_client_id, okta_client_secret]
    ):
        print("Missing required values in secrets.json.")
        return

    try:
        print(f"Retrieving metadata for bucket: {gcs_bucket_name}...")
        metadata = authenticate_with_okta_credentials(
            bucket_name=gcs_bucket_name,
            audience=gcp_audience,
            domain=okta_domain,
            client_id=okta_client_id,
            client_secret=okta_client_secret,
            impersonation_url=sa_impersonation_url,
        )
        print("--- SUCCESS! ---")
        print(json.dumps(metadata, indent=2))
    except Exception as e:
        print(f"Authentication or Request failed: {e}")


if __name__ == "__main__":
    main()
