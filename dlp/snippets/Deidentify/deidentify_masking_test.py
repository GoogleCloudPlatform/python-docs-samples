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

import deidentify_masking as deid

import pytest

HARMFUL_STRING = "My SSN is 372819127"
HARMLESS_STRING = "My favorite color is blue"
GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deidentify_with_mask(capsys: pytest.CaptureFixture) -> None:
    deid.deidentify_with_mask(
        GCLOUD_PROJECT, HARMFUL_STRING, ["US_SOCIAL_SECURITY_NUMBER"]
    )

    out, _ = capsys.readouterr()
    assert "My SSN is *********" in out


def test_deidentify_with_mask_ignore_insensitive_data(
    capsys: pytest.CaptureFixture,
) -> None:
    deid.deidentify_with_mask(
        GCLOUD_PROJECT, HARMLESS_STRING, ["US_SOCIAL_SECURITY_NUMBER"]
    )

    out, _ = capsys.readouterr()
    assert HARMLESS_STRING in out


def test_deidentify_with_mask_masking_character_specified(
    capsys: pytest.CaptureFixture,
) -> None:
    deid.deidentify_with_mask(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        masking_character="#",
    )

    out, _ = capsys.readouterr()
    assert "My SSN is #########" in out


def test_deidentify_with_mask_masking_number_specified(
    capsys: pytest.CaptureFixture,
) -> None:
    deid.deidentify_with_mask(
        GCLOUD_PROJECT,
        HARMFUL_STRING,
        ["US_SOCIAL_SECURITY_NUMBER"],
        number_to_mask=7,
    )

    out, _ = capsys.readouterr()
    assert "My SSN is *******27" in out
