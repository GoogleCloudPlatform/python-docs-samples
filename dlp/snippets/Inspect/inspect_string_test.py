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

import inspect_string as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_inspect_string(capsys: pytest.CaptureFixture) -> None:
    test_string = "My name is Gary Smith and my email is gary@example.com"

    inspect_content.inspect_string(
        GCLOUD_PROJECT,
        test_string,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: FIRST_NAME" in out
    assert "Info type: EMAIL_ADDRESS" in out
