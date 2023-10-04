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

import deidentify_table_condition_masking as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TABLE_DATA = {
    "header": ["age", "patient", "happiness_score"],
    "rows": [
        ["101", "Charles Dickens", "95"],
        ["22", "Jane Austen", "21"],
        ["90", "Mark Twain", "75"],
    ],
}


def test_deidentify_table_condition_masking(capsys: pytest.CaptureFixture) -> None:
    deid_list = ["happiness_score"]
    deid.deidentify_table_condition_masking(
        GCLOUD_PROJECT,
        TABLE_DATA,
        deid_list,
        condition_field="age",
        condition_operator="GREATER_THAN",
        condition_value=89,
    )
    out, _ = capsys.readouterr()
    assert 'string_value: "**"' in out
    assert 'string_value: "21"' in out


def test_deidentify_table_condition_masking_with_masking_character_specified(
    capsys: pytest.CaptureFixture,
) -> None:
    deid_list = ["happiness_score"]
    deid.deidentify_table_condition_masking(
        GCLOUD_PROJECT,
        TABLE_DATA,
        deid_list,
        condition_field="age",
        condition_operator="GREATER_THAN",
        condition_value=89,
        masking_character="#",
    )
    out, _ = capsys.readouterr()
    assert 'string_value: "##"' in out
    assert 'string_value: "21"' in out
