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

import re

import google
from _pytest.capture import CaptureFixture
from google.cloud import webrisk_v1

from webrisk.snippets import compute_threatlist_diff, search_hashes, search_uri, submit_uri

PROJECT = google.auth.default()[1]


def test_search_uri_with_threat(capsys: CaptureFixture):
    search_uri.search_uri("http://testsafebrowsing.appspot.com/s/malware.html", webrisk_v1.ThreatType.MALWARE)
    assert re.search("The URI has the following threat: ", capsys.readouterr().out)


def test_search_uri_without_threat(capsys: CaptureFixture):
    search_uri.search_uri("http://testsafebrowsing.appspot.com/malware.html", webrisk_v1.ThreatType.MALWARE)
    assert re.search("The URL is safe!", capsys.readouterr().out)


def test_submit_uri(capsys: CaptureFixture):
    submit_uri.submit_uri(PROJECT, "http://testsafebrowsing.appspot.com/s/malware.html")
    assert re.search("Submission response: ", capsys.readouterr().out)


def test_compute_threatdiff_list(capsys: CaptureFixture):
    compute_threatlist_diff.compute_threatlist_diff(webrisk_v1.ThreatType.MALWARE, b'', 1024, 1024, webrisk_v1.CompressionType.RAW)
    assert re.search("Obtained threat list diff.", capsys.readouterr().out)
