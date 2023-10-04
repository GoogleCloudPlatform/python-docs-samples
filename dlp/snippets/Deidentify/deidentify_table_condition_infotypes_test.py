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

import deidentify_table_condition_infotypes as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deidentify_table_condition_replace_with_info_types(
    capsys: pytest.CaptureFixture,
) -> None:
    deid_list = ["patient", "factoid"]
    table_data = {
        "header": ["age", "patient", "happiness_score", "factoid"],
        "rows": [
            [
                "101",
                "Charles Dickens",
                "95",
                "Charles Dickens name was a curse invented by Shakespeare.",
            ],
            ["22", "Jane Austen", "21", "There are 14 kisses in Jane Austen's novels."],
            ["90", "Mark Twain", "75", "Mark Twain loved cats."],
        ],
    }

    deid.deidentify_table_condition_replace_with_info_types(
        GCLOUD_PROJECT,
        table_data,
        deid_list,
        ["PERSON_NAME"],
        "age",
        "GREATER_THAN",
        89,
    )

    out, _ = capsys.readouterr()

    assert 'string_value: "Jane Austen"' in out
    assert "[PERSON_NAME] name was a curse invented by [PERSON_NAME]." in out
    assert "There are 14 kisses in Jane Austen\\'s novels." in out
    assert "[PERSON_NAME] loved cats." in out
