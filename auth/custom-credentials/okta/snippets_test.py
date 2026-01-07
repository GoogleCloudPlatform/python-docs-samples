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

import json
import os
import time
from unittest import mock
import urllib.parse

import pytest

import snippets

# --- Unit Tests ---


def test_init_url_cleaning():
    """Test that the token URL strips trailing slashes."""
    s1 = snippets.OktaClientCredentialsSupplier("https://okta.com/", "id", "sec")
    assert s1.okta_token_url == "https://okta.com/oauth2/default/v1/token"

    s2 = snippets.OktaClientCredentialsSupplier("https://okta.com", "id", "sec")
    assert s2.okta_token_url == "https://okta.com/oauth2/default/v1/token"


@mock.patch("requests.post")
def test_get_subject_token_fetch(mock_post):
    """Test fetching a new token from Okta."""
    supplier = snippets.OktaClientCredentialsSupplier("https://okta.com", "id", "sec")

    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "new-token", "expires_in": 3600}
    mock_post.return_value = mock_response

    token = supplier.get_subject_token(None, None)

    assert token == "new-token"
    mock_post.assert_called_once()

    # Verify args
    _, kwargs = mock_post.call_args
    assert kwargs["auth"] == ("id", "sec")

    sent_data = urllib.parse.parse_qs(kwargs["data"])
    assert sent_data["grant_type"][0] == "client_credentials"


@mock.patch("requests.post")
def test_get_subject_token_cached(mock_post):
    """Test that cached token is returned if valid."""
    supplier = snippets.OktaClientCredentialsSupplier("https://okta.com", "id", "sec")
    supplier.access_token = "cached-token"
    supplier.expiry_time = time.time() + 3600

    token = supplier.get_subject_token(None, None)

    assert token == "cached-token"
    mock_post.assert_not_called()


@mock.patch("snippets.auth_requests.AuthorizedSession")
@mock.patch("snippets.identity_pool.Credentials")
@mock.patch("snippets.OktaClientCredentialsSupplier")
def test_authenticate_unit_success(MockSupplier, MockCreds, MockSession):
    """Unit test for the main Okta auth flow."""
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "test-bucket"}

    mock_session_instance = MockSession.return_value
    mock_session_instance.get.return_value = mock_response

    metadata = snippets.authenticate_with_okta_credentials(
        bucket_name="test-bucket",
        audience="test-aud",
        domain="https://okta.com",
        client_id="id",
        client_secret="sec",
        impersonation_url=None,
    )

    assert metadata == {"name": "test-bucket"}
    MockSupplier.assert_called_once()
    MockCreds.assert_called_once()


# --- System Test ---


def test_authenticate_system():
    """
    System test that runs against the real API.
    Skips automatically if custom-credentials-okta-secrets.json is missing or incomplete.
    """
    if not os.path.exists("custom-credentials-okta-secrets.json"):
        pytest.skip(
            "Skipping system test: custom-credentials-okta-secrets.json not found."
        )

    with open("custom-credentials-okta-secrets.json", "r") as f:
        secrets = json.load(f)

    required_keys = [
        "gcp_workload_audience",
        "gcs_bucket_name",
        "okta_domain",
        "okta_client_id",
        "okta_client_secret",
    ]
    if not all(key in secrets for key in required_keys):
        pytest.skip(
            "Skipping system test: custom-credentials-okta-secrets.json is missing required keys."
        )

    # The main() function handles the auth flow and printing.
    # We mock the print function to verify the output.
    with mock.patch("builtins.print") as mock_print:
        snippets.main()

        # Check for the success message in the print output.
        output = "\n".join([call.args[0] for call in mock_print.call_args_list])
        assert "--- SUCCESS! ---" in output
