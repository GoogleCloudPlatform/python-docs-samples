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

import deidentify_table_bucketing as deid

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


def test_deidentify_table_bucketing(capsys: pytest.CaptureFixture) -> None:
    deid_list = ["happiness_score"]
    bucket_size = 10
    lower_bound = 0
    upper_bound = 100

    deid.deidentify_table_bucketing(
        GCLOUD_PROJECT,
        TABLE_DATA,
        deid_list,
        bucket_size,
        lower_bound,
        upper_bound,
    )

    out, _ = capsys.readouterr()
    assert 'string_value: "90:100"' in out
    assert 'string_value: "20:30"' in out
    assert 'string_value: "70:80"' in out
