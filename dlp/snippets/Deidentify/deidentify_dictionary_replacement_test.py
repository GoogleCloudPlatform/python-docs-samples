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

import deidentify_dictionary_replacement as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deindentify_with_dictionary_replacement(capsys: pytest.CaptureFixture) -> None:
    deid.deindentify_with_dictionary_replacement(
        GCLOUD_PROJECT,
        "My name is Alicia Abernathy, and my email address is aabernathy@example.com.",
        ["EMAIL_ADDRESS"],
        ["izumi@example.com", "alex@example.com", "tal@example.com"],
    )
    out, _ = capsys.readouterr()
    assert "aabernathy@example.com" not in out
    assert (
        "izumi@example.com" in out
        or "alex@example.com" in out
        or "tal@example.com" in out
    )
