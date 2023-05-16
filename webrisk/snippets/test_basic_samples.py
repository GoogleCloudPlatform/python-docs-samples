#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import base64
import hashlib
import re

from _pytest.capture import CaptureFixture
import google
from google.cloud import webrisk_v1

from .compute_threatlist_diff import compute_threatlist_diff
from .search_hashes import search_hashes
from .search_uri import search_uri
from .submit_uri import submit_uri

PROJECT = google.auth.default()[1]


def test_search_uri_with_threat() -> None:
    response = search_uri(
        "http://testsafebrowsing.appspot.com/s/malware.html",
        webrisk_v1.ThreatType.MALWARE,
    )
    assert response.threat.threat_types


def test_search_uri_without_threat() -> None:
    response = search_uri(
        "http://testsafebrowsing.appspot.com/malware.html",
        webrisk_v1.ThreatType.MALWARE,
    )
    assert not response.threat.threat_types


def test_submit_uri() -> None:
    malware_uri = "http://testsafebrowsing.appspot.com/s/malware.html"
    response = submit_uri(PROJECT, malware_uri)
    assert response.uri == malware_uri


def test_search_hashes() -> None:
    uri = "http://example.com"
    sha256 = hashlib.sha256()
    sha256.update(base64.urlsafe_b64encode(bytes(uri, "utf-8")))
    hex_string = sha256.digest()

    # The hash list may or may not be empty. Hence, no assertion is required as long as the code runs to completion.
    search_hashes(hex_string, webrisk_v1.ThreatType.MALWARE)


def test_compute_threatdiff_list() -> None:
    response = compute_threatlist_diff(
        webrisk_v1.ThreatType.MALWARE, b"", 1024, 1024, webrisk_v1.CompressionType.RAW
    )
    assert response.response_type
