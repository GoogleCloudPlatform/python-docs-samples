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

import deidentify_exception_list as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deidentify_with_exception_list(capsys: pytest.CaptureFixture) -> None:
    content_str = "jack@example.org accessed record of user: gary@example.org"
    exception_list = ["jack@example.org", "jill@example.org"]
    deid.deidentify_with_exception_list(
        GCLOUD_PROJECT, content_str, ["EMAIL_ADDRESS"], exception_list
    )

    out, _ = capsys.readouterr()

    assert "gary@example.org" not in out
    assert "jack@example.org accessed record of user: [EMAIL_ADDRESS]" in out
