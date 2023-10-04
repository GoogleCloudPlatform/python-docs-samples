# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import deidentify_replace_infotype as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deidentify_with_replace_infotype(capsys: pytest.CaptureFixture) -> None:
    url_to_redact = "https://cloud.google.com"
    deid.deidentify_with_replace_infotype(
        GCLOUD_PROJECT,
        "My favorite site is " + url_to_redact,
        ["URL"],
    )

    out, _ = capsys.readouterr()

    assert url_to_redact not in out
    assert "My favorite site is [URL]" in out
