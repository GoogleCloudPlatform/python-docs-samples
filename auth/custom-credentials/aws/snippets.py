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

# [START auth_custom_credential_supplier_aws]
import json
import os

import boto3
from google.auth import aws
from google.auth import exceptions
from google.auth.transport import requests as auth_requests


class CustomAwsSupplier(aws.AwsSecurityCredentialsSupplier):
    """Custom AWS Security Credentials Supplier using Boto3."""

    def __init__(self):
        """Initializes the Boto3 session, prioritizing environment variables for region."""
        # Explicitly read the region from the environment first.
        region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")

        # If region is None, Boto3's discovery chain will be used when needed.
        self.session = boto3.Session(region_name=region)
        self._cached_region = None

    def get_aws_region(self, context, request) -> str:
        """Returns the AWS region using Boto3's default provider chain."""
        if self._cached_region:
            return self._cached_region

        self._cached_region = self.session.region_name

        if not self._cached_region:
            raise exceptions.GoogleAuthError(
                "Boto3 was unable to resolve an AWS region."
            )

        return self._cached_region

    def get_aws_security_credentials(
        self, context, request=None
    ) -> aws.AwsSecurityCredentials:
        """Retrieves AWS security credentials using Boto3's default provider chain."""
        creds = self.session.get_credentials()
        if not creds:
            raise exceptions.GoogleAuthError(
                "Unable to resolve AWS credentials from Boto3."
            )

        return aws.AwsSecurityCredentials(
            access_key_id=creds.access_key,
            secret_access_key=creds.secret_key,
            session_token=creds.token,
        )


def authenticate_with_aws_credentials(bucket_name, audience, impersonation_url=None):
    """Authenticates using the custom AWS supplier and gets bucket metadata.

    Returns:
        dict: The bucket metadata response from the Google Cloud Storage API.
    """

    # 1. Instantiate the custom supplier.
    custom_supplier = CustomAwsSupplier()

    # 2. Instantiate the AWS Credentials object.
    credentials = aws.Credentials(
        audience=audience,
        subject_token_type="urn:ietf:params:aws:token-type:aws4_request",
        service_account_impersonation_url=impersonation_url,
        aws_security_credentials_supplier=custom_supplier,
        scopes=["https://www.googleapis.com/auth/devstorage.read_write"],
    )

    # 3. Create an authenticated session.
    authed_session = auth_requests.AuthorizedSession(credentials)

    # 4. Make the API Request.
    bucket_url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}"

    response = authed_session.get(bucket_url)
    response.raise_for_status()

    return response.json()


# [END auth_custom_credential_supplier_aws]


def _load_config_from_file():
    """
    If a local secrets file is present, load it into the environment.
    This is a "just-in-time" configuration for local development. These
    variables are only set for the current process and are not exposed to the
    shell.
    """
    if os.path.exists("custom-credentials-aws-secrets.json"):
        with open("custom-credentials-aws-secrets.json", "r") as f:
            secrets = json.load(f)

        os.environ["AWS_ACCESS_KEY_ID"] = secrets.get("aws_access_key_id", "")
        os.environ["AWS_SECRET_ACCESS_KEY"] = secrets.get("aws_secret_access_key", "")
        os.environ["AWS_REGION"] = secrets.get("aws_region", "")
        os.environ["GCP_WORKLOAD_AUDIENCE"] = secrets.get("gcp_workload_audience", "")
        os.environ["GCS_BUCKET_NAME"] = secrets.get("gcs_bucket_name", "")
        os.environ["GCP_SERVICE_ACCOUNT_IMPERSONATION_URL"] = secrets.get(
            "gcp_service_account_impersonation_url", ""
        )


def main():

    # Reads the custom-credentials-aws-secrets.json if running locally.
    _load_config_from_file()

    # Now, read the configuration from the environment. In a local run, these
    # will be the values we just set. In a containerized run, they will be
    # the values provided by the environment.
    gcp_audience = os.getenv("GCP_WORKLOAD_AUDIENCE")
    sa_impersonation_url = os.getenv("GCP_SERVICE_ACCOUNT_IMPERSONATION_URL")
    gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")

    if not all([gcp_audience, gcs_bucket_name]):
        print(
            "Required configuration missing. Please provide it in a "
            "custom-credentials-aws-secrets.json file or as environment variables: "
            "GCP_WORKLOAD_AUDIENCE, GCS_BUCKET_NAME"
        )
        return

    try:
        print(f"Retrieving metadata for bucket: {gcs_bucket_name}...")
        metadata = authenticate_with_aws_credentials(
            gcs_bucket_name, gcp_audience, sa_impersonation_url
        )
        print("--- SUCCESS! ---")
        print(json.dumps(metadata, indent=2))
    except Exception as e:
        print(f"Authentication or Request failed: {e}")


if __name__ == "__main__":
    main()
