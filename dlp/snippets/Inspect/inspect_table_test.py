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

import inspect_table as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_inspect_table(capsys: pytest.CaptureFixture) -> None:
    test_tabular_data = {
        "header": ["email", "phone number"],
        "rows": [
            ["robertfrost@xyz.com", "4232342345"],
            ["johndoe@pqr.com", "4253458383"],
        ],
    }

    inspect_content.inspect_table(
        GCLOUD_PROJECT,
        test_tabular_data,
        ["PHONE_NUMBER", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
    assert "Info type: EMAIL_ADDRESS" in out
