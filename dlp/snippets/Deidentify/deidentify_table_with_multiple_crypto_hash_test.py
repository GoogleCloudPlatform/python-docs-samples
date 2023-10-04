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

import deidentify_table_with_multiple_crypto_hash as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


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

    deid.deidentify_table_with_multiple_crypto_hash(
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
