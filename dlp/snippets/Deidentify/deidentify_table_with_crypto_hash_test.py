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

import deidentify_table_with_crypto_hash as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deidentify_table_with_crypto_hash(capsys: pytest.CaptureFixture) -> None:
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

    deid.deidentify_table_with_crypto_hash(
        GCLOUD_PROJECT,
        table_data,
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        "TRANSIENT-CRYPTO-KEY",
    )

    out, _ = capsys.readouterr()

    assert "abby_abernathy@example.org" not in out
    assert "858-555-0222" not in out
