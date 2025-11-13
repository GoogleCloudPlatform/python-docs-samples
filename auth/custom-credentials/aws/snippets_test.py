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
import unittest
from unittest.mock import MagicMock, patch

from google.auth import exceptions
import requests

# Import the module to be tested.
# NOTE: Update 'main' to the actual filename if different.
import snippets as app_module

class TestCustomAwsSupplier(unittest.TestCase):
    
    @patch.dict(os.environ, {"AWS_REGION": "us-west-2"})
    @patch("boto3.Session")
    def test_init_priority_env_var(self, mock_boto_session):
        """Test that AWS_REGION env var takes priority during init."""
        app_module.CustomAwsSupplier()
        # Verify boto3.Session was initialized with the region from env
        mock_boto_session.assert_called_with(region_name="us-west-2")


    @patch.dict(os.environ, {}, clear=True)
    @patch("boto3.Session")
    def test_get_aws_region_missing(self, mock_boto_session):
        """Test that an error is raised if region cannot be resolved."""
        mock_session_instance = mock_boto_session.return_value
        # Simulate Boto3 failing to find a region
        mock_session_instance.region_name = None

        supplier = app_module.CustomAwsSupplier()

        with self.assertRaisesRegex(exceptions.GoogleAuthError, "unable to resolve an AWS region"):
            supplier.get_aws_region(None, None)

    @patch("boto3.Session")
    def test_get_aws_security_credentials_success(self, mock_boto_session):
        """Test successful retrieval of AWS credentials."""
        mock_session_instance = mock_boto_session.return_value
        
        # Mock the credentials object returned by boto3
        mock_creds = MagicMock()
        mock_creds.access_key = "test-access-key"
        mock_creds.secret_key = "test-secret-key"
        mock_creds.token = "test-session-token"
        mock_session_instance.get_credentials.return_value = mock_creds

        supplier = app_module.CustomAwsSupplier()
        creds = supplier.get_aws_security_credentials(None)

        self.assertEqual(creds.access_key_id, "test-access-key")
        self.assertEqual(creds.secret_access_key, "test-secret-key")
        self.assertEqual(creds.session_token, "test-session-token")

    @patch("boto3.Session")
    def test_get_aws_security_credentials_none(self, mock_boto_session):
        """Test handling when Boto3 returns no credentials."""
        mock_session_instance = mock_boto_session.return_value
        mock_session_instance.get_credentials.return_value = None

        supplier = app_module.CustomAwsSupplier()

        with self.assertRaisesRegex(exceptions.GoogleAuthError, "Unable to resolve AWS credentials"):
            supplier.get_aws_security_credentials(None)


class TestAuthenticateLogic(unittest.TestCase):

    @patch("snippets.auth_requests.AuthorizedSession")
    @patch("snippets.aws.Credentials")
    @patch("snippets.CustomAwsSupplier")
    def test_authenticate_success(self, MockSupplier, MockAwsCreds, MockSession):
        """Test the success path of the main logic function."""
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"kind": "storage#bucket", "name": "my-bucket"}
        
        mock_session_instance = MockSession.return_value
        mock_session_instance.get.return_value = mock_response

        # Run the function
        app_module.authenticate_with_aws_credentials(
            bucket_name="my-bucket",
            audience="//iam.googleapis.com/...",
            impersonation_url="https://..."
        )

        # Assertions
        MockSupplier.assert_called_once()
        MockAwsCreds.assert_called_once()
        # Verify bucket URL was constructed correctly
        mock_session_instance.get.assert_called_with("https://storage.googleapis.com/storage/v1/b/my-bucket")
        mock_response.raise_for_status.assert_called_once()

if __name__ == "__main__":
    unittest.main()