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

import pytest

import deid_table

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
TABLE_DATA = {
    "header": ["age", "patient", "happiness_score"],
    "rows": [
        ["101", "Charles Dickens", "95"],
        ["22", "Jane Austen", "21"],
        ["90", "Mark Twain", "75"],
    ],
}


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

    deid_table.deidentify_table_with_fpe(
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

    deid_table.reidentify_table_with_fpe(
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


def test_deidentify_table_with_crypro_hash(capsys: pytest.CaptureFixture) -> None:
    table_data = {
        "header": ["user_id", "comments"],
        "rows": [
            [
                "abby_abernathy@example.org",
                "my email is abby_abernathy@example.org and phone is 858-555-0222",
            ],
            [
                "bert_beauregard@example.org",
                "my email is bert_beauregard@example.org and phone is 858-555-0223",
            ],
            [
                "cathy_crenshaw@example.org",
                "my email is cathy_crenshaw@example.org and phone is 858-555-0224",
            ],
        ],
    }

    deid_table.deidentify_table_with_crypto_hash(
        GCLOUD_PROJECT,
        table_data,
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        "TRANSIENT-CRYPTO-KEY",
    )

    out, _ = capsys.readouterr()

    assert "abby_abernathy@example.org" not in out
    assert "858-555-0222" not in out


def test_deidentify_table_with_multiple_crypto_hash(
    capsys: pytest.CaptureFixture,
) -> None:
    table_data = {
        "header": ["user_id", "comments"],
        "rows": [
            [
                "user1@example.org",
                "my email is user1@example.org and phone is 858-333-2222",
            ],
            [
                "abbyabernathy1",
                "my userid is abbyabernathy1 and my email is aabernathy@example.com",
            ],
        ],
    }

    deid_table.deidentify_table_with_multiple_crypto_hash(
        GCLOUD_PROJECT,
        table_data,
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        "TRANSIENT-CRYPTO-KEY-1",
        "TRANSIENT-CRYPTO-KEY-2",
        ["user_id"],
        ["comments"],
    )

    out, _ = capsys.readouterr()

    assert "user1@example.org" not in out
    assert "858-555-0222" not in out
    assert 'string_value: "abbyabernathy1"' not in out
    assert "my userid is abbyabernathy1" in out
    assert "aabernathy@example.com" not in out


def test_deidentify_table_bucketing(capsys: pytest.CaptureFixture) -> None:
    deid_list = ["happiness_score"]
    bucket_size = 10
    lower_bound = 0
    upper_bound = 100

    deid_table.deidentify_table_bucketing(
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


def test_deidentify_table_primitive_bucketing(capsys: pytest.CaptureFixture) -> None:

    deid_table.deidentify_table_primitive_bucketing(
        GCLOUD_PROJECT,
    )

    out, _ = capsys.readouterr()
    assert "string_value: \"High\"" in out
    assert "string_value: \"Low\"" in out


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

    deid_table.deidentify_table_condition_replace_with_info_types(
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


def test_deidentify_table_condition_masking(capsys: pytest.CaptureFixture) -> None:
    deid_list = ["happiness_score"]
    deid_table.deidentify_table_condition_masking(
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
    deid_table.deidentify_table_condition_masking(
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


def test_deidentify_table_replace_with_info_types(
    capsys: pytest.CaptureFixture,
) -> None:
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

    deid_table.deidentify_table_replace_with_info_types(
        GCLOUD_PROJECT,
        table_data,
        ["PERSON_NAME"],
        ["patient", "factoid"],
    )

    out, _ = capsys.readouterr()

    assert 'string_value: "[PERSON_NAME]"' in out
    assert "[PERSON_NAME] name was a curse invented by [PERSON_NAME]." in out
    assert "There are 14 kisses in [PERSON_NAME] novels." in out
    assert "[PERSON_NAME] loved cats." in out


def test_deidentify_table_suppress_row(capsys: pytest.CaptureFixture) -> None:
    deid_table.deidentify_table_suppress_row(
        GCLOUD_PROJECT, TABLE_DATA, "age", "GREATER_THAN", 89
    )

    out, _ = capsys.readouterr()

    assert 'string_value: "Charles Dickens"' not in out
    assert 'string_value: "Jane Austen"' in out
    assert 'string_value: "Mark Twain"' not in out
