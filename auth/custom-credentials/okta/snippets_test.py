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

import unittest
import urllib.parse
from unittest.mock import MagicMock, patch

import snippets as app_module


class TestOktaClientCredentialsSupplier(unittest.TestCase):
    
    def setUp(self):
        self.domain = "https://okta.example.com"
        self.client_id = "test-id"
        self.client_secret = "test-secret"
        self.supplier = app_module.OktaClientCredentialsSupplier(
            self.domain, self.client_id, self.client_secret
        )

    def test_init_url_cleaning(self):
        """Test that the token URL strips trailing slashes."""
        # Case 1: Trailing slash
        s1 = app_module.OktaClientCredentialsSupplier("https://okta.com/", "id", "sec")
        self.assertEqual(s1.okta_token_url, "https://okta.com/oauth2/default/v1/token")
        
        # Case 2: No trailing slash
        s2 = app_module.OktaClientCredentialsSupplier("https://okta.com", "id", "sec")
        self.assertEqual(s2.okta_token_url, "https://okta.com/oauth2/default/v1/token")

    @patch("requests.post")
    def test_get_subject_token_fetch(self, mock_post):
        """Test fetching a new token from Okta."""
        # Mock the Okta response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new-token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response

        # Execute
        token = self.supplier.get_subject_token(None, None)

        # Verify
        self.assertEqual(token, "new-token")
        self.assertEqual(self.supplier.access_token, "new-token")
        
        # Check that requests.post was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["auth"], (self.client_id, self.client_secret))
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/x-www-form-urlencoded")
        
        # The script encodes data using urllib, so we decode it to verify contents
        sent_data = urllib.parse.parse_qs(kwargs["data"])
        self.assertEqual(sent_data["grant_type"][0], "client_credentials")
        self.assertEqual(sent_data["scope"][0], "gcp.test.read")


class TestAuthenticationFlow(unittest.TestCase):

    @patch("snippets.auth_requests.AuthorizedSession")
    @patch("snippets.identity_pool.Credentials")
    @patch("snippets.OktaClientCredentialsSupplier")
    def test_authenticate_success(self, MockSupplier, MockCreds, MockSession):
        """Test the main logic flow for successful authentication."""
        # Setup Mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"kind": "storage#bucket", "name": "test-bucket"}
        
        mock_session_instance = MockSession.return_value
        mock_session_instance.get.return_value = mock_response

        # Execute
        app_module.authenticate_with_okta_credentials(
            bucket_name="test-bucket",
            audience="test-aud",
            domain="https://okta.com",
            client_id="id",
            client_secret="sec",
            impersonation_url=None
        )

        # Verify
        MockSupplier.assert_called_once()
        MockCreds.assert_called_once()
        mock_session_instance.get.assert_called_with(
            "https://storage.googleapis.com/storage/v1/b/test-bucket"
        )
        mock_response.raise_for_status.assert_called_once()


if __name__ == "__main__":
    unittest.main()