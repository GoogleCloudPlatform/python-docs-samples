# Copyright 2025 Google LLC
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

import os
from unittest import mock

import pytest

import snippets

# --- Unit Tests ---


@mock.patch.dict(os.environ, {"AWS_REGION": "us-west-2"})
@mock.patch("boto3.Session")
def test_init_priority_env_var(mock_boto_session):
    """Test that AWS_REGION env var takes priority during init."""
    snippets.CustomAwsSupplier()
    mock_boto_session.assert_called_with(region_name="us-west-2")


@mock.patch.dict(os.environ, {}, clear=True)
@mock.patch("boto3.Session")
def test_get_aws_region_caching(mock_boto_session):
    """Test that get_aws_region caches the result from Boto3."""
    mock_session_instance = mock_boto_session.return_value
    mock_session_instance.region_name = "us-east-1"

    supplier = snippets.CustomAwsSupplier()

    # First call should hit the session
    region = supplier.get_aws_region(None, None)
    assert region == "us-east-1"

    # Change the mock to ensure we aren't calling it again
    mock_session_instance.region_name = "us-west-2"

    # Second call should return the cached value
    region2 = supplier.get_aws_region(None, None)
    assert region2 == "us-east-1"


@mock.patch("boto3.Session")
def test_get_aws_security_credentials_success(mock_boto_session):
    """Test successful retrieval of AWS credentials."""
    mock_session_instance = mock_boto_session.return_value

    mock_creds = mock.MagicMock()
    mock_creds.access_key = "test-key"
    mock_creds.secret_key = "test-secret"
    mock_creds.token = "test-token"
    mock_session_instance.get_credentials.return_value = mock_creds

    supplier = snippets.CustomAwsSupplier()
    creds = supplier.get_aws_security_credentials(None)

    assert creds.access_key_id == "test-key"
    assert creds.secret_access_key == "test-secret"
    assert creds.session_token == "test-token"


@mock.patch("snippets.auth_requests.AuthorizedSession")
@mock.patch("snippets.aws.Credentials")
@mock.patch("snippets.CustomAwsSupplier")
def test_authenticate_unit_success(MockSupplier, MockAwsCreds, MockSession):
    """Unit test for the main flow using mocks."""
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "my-bucket"}

    mock_session_instance = MockSession.return_value
    mock_session_instance.get.return_value = mock_response

    result = snippets.authenticate_with_aws_credentials(
        bucket_name="my-bucket",
        audience="//iam.googleapis.com/...",
        impersonation_url=None,
    )

    assert result == {"name": "my-bucket"}
    MockSupplier.assert_called_once()
    MockAwsCreds.assert_called_once()


# --- System Test (Integration) ---


def test_authenticate_system():
    """
    System test that runs against the real API.
    Skips automatically if required environment variables are missing.
    """
    required_env = ["GCP_WORKLOAD_AUDIENCE", "GCS_BUCKET_NAME", "AWS_ACCESS_KEY_ID"]
    if not all(os.getenv(var) for var in required_env):
        pytest.skip(
            "Skipping system test: missing required env vars (GCP/AWS credentials)."
        )

    audience = os.getenv("GCP_WORKLOAD_AUDIENCE")
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    impersonation_url = os.getenv("GCP_SERVICE_ACCOUNT_IMPERSONATION_URL")

    # This calls the real API
    metadata = snippets.authenticate_with_aws_credentials(
        bucket_name=bucket_name, audience=audience, impersonation_url=impersonation_url
    )

    assert metadata is not None
    assert metadata.get("name") == bucket_name
