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
import base64
import os

import deidentify_table_fpe as deid

import pytest

import reidentify_table_fpe as reid

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
UNWRAPPED_KEY = "YWJjZGVmZ2hpamtsbW5vcA=="
WRAPPED_KEY = (
    "CiQAz0hX4+go8fJwn80Fr8pVImwx+tmZdqU7JL+7TN/S5JxBU9gSSQDhFHpFVy"
    "uzJps0YH9ls480mU+JLG7jI/0lL04i6XJRWqmI6gUSZRUtECYcLH5gXK4SXHlL"
    "rotx7Chxz/4z7SIpXFOBY61z0/U="
)
KEY_NAME = (
    f"projects/{GCLOUD_PROJECT}/locations/global/keyRings/"
    "dlp-test/cryptoKeys/dlp-test"
)


def test_deidentify_and_reidentify_table_with_fpe(
    capsys: pytest.CaptureFixture,
) -> None:
    table_data = {
        "header": ["employee_id", "date", "compensation"],
        "rows": [
            ["11111", "2015", "$10"],
            ["22222", "2016", "$20"],
            ["33333", "2016", "$15"],
        ],
    }

    deid.deidentify_table_with_fpe(
        GCLOUD_PROJECT,
        table_data["header"],
        table_data["rows"],
        ["employee_id"],
        alphabet="NUMERIC",
        wrapped_key=base64.b64decode(WRAPPED_KEY),
        key_name=KEY_NAME,
    )

    out, _ = capsys.readouterr()
    assert "11111" not in out
    assert "22222" not in out

    response = out.split(":")[1:]

    deid_col_id = response.index(' "employee_id"\n}\nheaders {\n  name')
    total_columns = len(table_data["header"])
    total_rows = len(table_data["rows"][0])

    deid_emp_ids = [
        response[i].split("\n")[0][2:-1]
        for i in range(deid_col_id + total_columns, len(response), total_columns)
    ]

    for i in range(total_rows):
        table_data["rows"][i][deid_col_id - 1] = deid_emp_ids[i]

    reid.reidentify_table_with_fpe(
        GCLOUD_PROJECT,
        table_data["header"],
        table_data["rows"],
        ["employee_id"],
        alphabet="NUMERIC",
        wrapped_key=base64.b64decode(WRAPPED_KEY),
        key_name=KEY_NAME,
    )

    out, _ = capsys.readouterr()
    assert "11111" in out
    assert "22222" in out
