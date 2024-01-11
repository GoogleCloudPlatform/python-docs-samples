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

import deidentify_free_text_with_fpe_using_surrogate as deid

import pytest


GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
UNWRAPPED_KEY = "YWJjZGVmZ2hpamtsbW5vcA=="


def test_deidentify_free_text_with_fpe_using_surrogate(
    capsys: pytest.CaptureFixture,
) -> None:
    labeled_fpe_string = "My phone number is 4359916732"

    deid.deidentify_free_text_with_fpe_using_surrogate(
        GCLOUD_PROJECT,
        labeled_fpe_string,
        info_type="PHONE_NUMBER",
        surrogate_type="PHONE_TOKEN",
        unwrapped_key=UNWRAPPED_KEY,
        alphabet="NUMERIC",
    )

    out, _ = capsys.readouterr()

    assert "PHONE_TOKEN" in out
    assert "My phone number is" in out
    assert "4359916732" not in out
