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
import sys

import boto3
from dotenv import load_dotenv
from google.auth.aws import AwsSecurityCredentials, AwsSecurityCredentialsSupplier
from google.auth.aws import Credentials as AwsCredentials
from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import AuthorizedSession

load_dotenv()


class CustomAwsSupplier(AwsSecurityCredentialsSupplier):
    """Custom AWS Security Credentials Supplier."""

    def __init__(self) -> None:
        """Initializes the Boto3 session, prioritizing environment variables for region."""
        # Explicitly read the region from the environment first. This ensures that
        # a value from a .env file is picked up reliably for local testing.
        region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")

        # If region is None, Boto3's discovery chain will be used when needed.
        self.session = boto3.Session(region_name=region)
        self._cached_region = None
        print(f"[INFO] CustomAwsSupplier initialized. Region from env: {region}")

    def get_aws_region(self, context: object, request: object) -> str:
        """Returns the AWS region using Boto3's default provider chain."""
        if self._cached_region:
            return self._cached_region

        # Accessing region_name will use the value from the constructor if provided,
        # otherwise it triggers Boto3's lazy-loading discovery (e.g., metadata service).
        self._cached_region = self.session.region_name

        if not self._cached_region:
            print("[ERROR] Boto3 was unable to resolve an AWS region.", file=sys.stderr)
            raise GoogleAuthError("Boto3 was unable to resolve an AWS region.")

        print(f"[INFO] Boto3 resolved AWS Region: {self._cached_region}")
        return self._cached_region

    def get_aws_security_credentials(self, context: object, request: object = None) -> AwsSecurityCredentials:
        """Retrieves AWS security credentials using Boto3's default provider chain."""
        aws_credentials = self.session.get_credentials()
        if not aws_credentials:
            print("[ERROR] Unable to resolve AWS credentials.", file=sys.stderr)
            raise GoogleAuthError("Unable to resolve AWS credentials from the provider chain.")

        # Instead of printing the whole key, mask everything but the last 4 characters
        masked_access_key = f"{'*' * 16}{aws_credentials.access_key[-4:]}"
        print(f"[INFO] Resolved AWS Access Key ID: {masked_access_key}")

        return AwsSecurityCredentials(
            access_key_id=aws_credentials.access_key,
            secret_access_key=aws_credentials.secret_key,
            session_token=aws_credentials.token,
        )


def main() -> None:
    """Main function to demonstrate the custom AWS supplier."""
    print("--- Starting Script ---")

    gcp_audience = os.getenv("GCP_WORKLOAD_AUDIENCE")
    sa_impersonation_url = os.getenv("GCP_SERVICE_ACCOUNT_IMPERSONATION_URL")
    gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")

    print(f"GCP_WORKLOAD_AUDIENCE: {gcp_audience}")
    print(f"GCS_BUCKET_NAME: {gcs_bucket_name}")

    if not all([gcp_audience, sa_impersonation_url, gcs_bucket_name]):
        print("[ERROR] Missing required environment variables.", file=sys.stderr)
        raise GoogleAuthError("Missing required environment variables.")

    custom_supplier = CustomAwsSupplier()

    credentials = AwsCredentials(
        audience=gcp_audience,
        subject_token_type="urn:ietf:params:aws:token-type:aws4_request",
        service_account_impersonation_url=sa_impersonation_url,
        aws_security_credentials_supplier=custom_supplier,
        scopes=['https://www.googleapis.com/auth/devstorage.read_write'],
    )

    bucket_url = f"https://storage.googleapis.com/storage/v1/b/{gcs_bucket_name}"
    print(f"Request URL: {bucket_url}")

    authed_session = AuthorizedSession(credentials)
    try:
        print("Attempting to make authenticated request to Google Cloud Storage...")
        res = authed_session.get(bucket_url)
        res.raise_for_status()
        print("\n--- SUCCESS! ---")
        print("Successfully authenticated and retrieved bucket data:")
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print("--- FAILED --- ", file=sys.stderr)
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
