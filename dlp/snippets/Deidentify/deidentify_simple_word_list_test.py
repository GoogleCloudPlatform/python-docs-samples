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

import deidentify_simple_word_list as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deidentify_with_simple_word_list(capsys: pytest.CaptureFixture) -> None:
    deid.deidentify_with_simple_word_list(
        GCLOUD_PROJECT,
        "Patient was seen in RM-YELLOW then transferred to rm green.",
        "CUSTOM_ROOM_ID",
        ["RM-GREEN", "RM-YELLOW", "RM-ORANGE"],
    )

    out, _ = capsys.readouterr()

    assert (
        "Patient was seen in [CUSTOM_ROOM_ID] then transferred to [CUSTOM_ROOM_ID]"
        in out
    )


def test_deidentify_with_simple_word_list_ignores_insensitive_data(
    capsys: pytest.CaptureFixture,
) -> None:
    deid.deidentify_with_simple_word_list(
        GCLOUD_PROJECT,
        "Patient was seen in RM-RED then transferred to rm green",
        "CUSTOM_ROOM_ID",
        ["RM-GREEN", "RM-YELLOW", "RM-ORANGE"],
    )

    out, _ = capsys.readouterr()

    assert "Patient was seen in RM-RED then transferred to [CUSTOM_ROOM_ID]" in out
