# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import get_google_ip_ranges

import netaddr
import pytest

@pytest.fixture
def sample_goog_data() -> dict:
    """Returns sample goog.json dictionary payload for testing."""
    return {
        "syncToken": "1631120724291",
        "creationTime": "2021-09-08T10:05:24.291305",
        "prefixes": [
            {"ipv4Prefix": "8.8.4.0/24"},
            {"ipv4Prefix": "34.128.208.0/12"},
            {"ipv4Prefix": "8.35.192.0/20"},
            {"ipv6Prefix": "2600:1900::/32"},
        ],
    }


@pytest.fixture
def sample_cloud_data() -> dict:
    """Returns sample cloud.json dictionary payload for testing."""
    return {
        "syncToken": "1631120724291",
        "creationTime": "2021-09-08T00:00:00.000001",
        "prefixes": [
            {
                "ipv4Prefix": "8.8.4.0/16",
                "service": "Google Cloud",
                "scope": "asia-east1",
            },
            {
                "ipv4Prefix": "34.128.208.0/16",
                "service": "Google Cloud",
                "scope": "asia-east1",
            },
        ],
    }


def test_get_data_success(
    sample_goog_data: dict, capsys: pytest.CaptureFixture
) -> None:
    """Tests that get_data successfully parses IPv4 and IPv6 prefixes into an IPSet."""
    # Arrange
    mock_response = io.BytesIO(json.dumps(sample_goog_data).encode("utf-8"))
    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_response

    # Act
    with patch("get_google_ip_ranges.urlopen", return_value=mock_context_manager):
        result = get_google_ip_ranges.get_data(
            "https://www.gstatic.com/ipranges/goog.json"
        )

    # Assert
    assert isinstance(result, netaddr.IPSet)
    assert netaddr.IPNetwork("8.8.4.0/24") in result
    assert netaddr.IPNetwork("8.35.192.0/20") in result
    assert netaddr.IPNetwork("2600:1900::/32") in result

    captured = capsys.readouterr()
    assert "published: 2021-09-08T10:05:24.291305" in captured.out


def test_get_data_url_error(capsys: pytest.CaptureFixture) -> None:
    """Tests that get_data handles network errors (URLError) gracefully."""
    # Act
    with patch(
        "get_google_ip_ranges.urlopen", side_effect=URLError("Connection failed")
    ):
        result = get_google_ip_ranges.get_data(
            "https://www.gstatic.com/ipranges/goog.json"
        )

    # Assert
    assert result is None
    captured = capsys.readouterr()
    assert "ERROR: Failed to fetch or parse" in captured.out


def test_get_data_json_decode_error(capsys: pytest.CaptureFixture) -> None:
    """Tests that get_data handles malformed JSON gracefully."""
    # Arrange
    mock_response = io.BytesIO(b"not-a-valid-json-document")
    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_response

    # Act
    with patch("get_google_ip_ranges.urlopen", return_value=mock_context_manager):
        result = get_google_ip_ranges.get_data(
            "https://www.gstatic.com/ipranges/goog.json"
        )

    # Assert
    assert result is None
    captured = capsys.readouterr()
    assert "ERROR: Failed to fetch or parse" in captured.out


def test_get_data_non_dict_json(capsys: pytest.CaptureFixture) -> None:
    """Tests that get_data handles non-dictionary JSON payloads gracefully."""
    # Arrange
    mock_response = io.BytesIO(json.dumps(["unexpected", "list"]).encode("utf-8"))
    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_response

    # Act
    with patch("get_google_ip_ranges.urlopen", return_value=mock_context_manager):
        result = get_google_ip_ranges.get_data(
            "https://www.gstatic.com/ipranges/goog.json"
        )

    # Assert
    assert result is None
    captured = capsys.readouterr()
    assert "ERROR: Expected JSON object" in captured.out


def test_get_data_invalid_prefix_entry(capsys: pytest.CaptureFixture) -> None:
    """Tests that get_data skips malformed prefix entries gracefully."""
    # Arrange
    payload = {
        "creationTime": "2026-01-01T00:00:00",
        "prefixes": [
            {"ipv4Prefix": "8.8.8.0/24"},
            {"ipv4Prefix": "not-a-valid-cidr"},
            "invalid_non_dict_entry",
        ],
    }
    mock_response = io.BytesIO(json.dumps(payload).encode("utf-8"))
    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_response

    # Act
    with patch("get_google_ip_ranges.urlopen", return_value=mock_context_manager):
        result = get_google_ip_ranges.get_data(
            "https://www.gstatic.com/ipranges/goog.json"
        )

    # Assert
    assert isinstance(result, netaddr.IPSet)
    assert netaddr.IPNetwork("8.8.8.0/24") in result
    captured = capsys.readouterr()
    assert "WARNING: Skipping invalid prefix" in captured.out


def test_get_data_timeout_error(capsys: pytest.CaptureFixture) -> None:
    """Tests that get_data handles socket timeouts gracefully."""
    # Act
    with patch(
        "get_google_ip_ranges.urlopen",
        side_effect=TimeoutError("Request timed out"),
    ):
        result = get_google_ip_ranges.get_data(
            "https://www.gstatic.com/ipranges/goog.json"
        )

    # Assert
    assert result is None
    captured = capsys.readouterr()
    assert "ERROR: Failed to fetch or parse" in captured.out


def test_main_success(
    sample_goog_data: dict,
    sample_cloud_data: dict,
    capsys: pytest.CaptureFixture,
) -> None:
    """Tests that main() computes (goog - cloud) and outputs expected CIDRs."""

    # Arrange
    def mock_get_data_side_effect(url: str) -> netaddr.IPSet:
        if "goog.json" in url:
            cidrs = netaddr.IPSet()
            for prefix in sample_goog_data["prefixes"]:
                if "ipv4Prefix" in prefix:
                    cidrs.add(prefix["ipv4Prefix"])
                if "ipv6Prefix" in prefix:
                    cidrs.add(prefix["ipv6Prefix"])
            return cidrs
        elif "cloud.json" in url:
            cidrs = netaddr.IPSet()
            for prefix in sample_cloud_data["prefixes"]:
                if "ipv4Prefix" in prefix:
                    cidrs.add(prefix["ipv4Prefix"])
                if "ipv6Prefix" in prefix:
                    cidrs.add(prefix["ipv6Prefix"])
            return cidrs
        return netaddr.IPSet()

    # Act
    with patch("get_google_ip_ranges.get_data", side_effect=mock_get_data_side_effect):
        get_google_ip_ranges.main()

    # Assert
    captured = capsys.readouterr()
    assert "IP ranges for Google APIs and services default domains:" in captured.out
    assert "8.35.192.0/20" in captured.out
    assert "2600:1900::/32" in captured.out


def test_main_failure_raises_value_error() -> None:
    """Tests that main() raises ValueError when a feed download fails."""
    with patch("get_google_ip_ranges.get_data", return_value=None):
        with pytest.raises(ValueError, match="ERROR: Could not process data from"):
            get_google_ip_ranges.main()