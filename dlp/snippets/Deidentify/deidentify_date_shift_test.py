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
import shutil
import tempfile
from typing import Iterator, TextIO

import deidentify_date_shift as deid

import pytest


GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
WRAPPED_KEY = (
    "CiQAz0hX4+go8fJwn80Fr8pVImwx+tmZdqU7JL+7TN/S5JxBU9gSSQDhFHpFVy"
    "uzJps0YH9ls480mU+JLG7jI/0lL04i6XJRWqmI6gUSZRUtECYcLH5gXK4SXHlL"
    "rotx7Chxz/4z7SIpXFOBY61z0/U="
)
KEY_NAME = (
    f"projects/{GCLOUD_PROJECT}/locations/global/keyRings/"
    "dlp-test/cryptoKeys/dlp-test"
)
CSV_FILE = os.path.join(os.path.dirname(__file__), "../resources/dates.csv")
DATE_SHIFTED_AMOUNT = 30
DATE_FIELDS = ["birth_date", "register_date"]
CSV_CONTEXT_FIELD = "name"


@pytest.fixture(scope="module")
def tempdir() -> Iterator[TextIO]:
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


def test_deidentify_with_date_shift(
    tempdir: TextIO, capsys: pytest.CaptureFixture
) -> None:
    output_filepath = os.path.join(tempdir, "dates-shifted.csv")

    deid.deidentify_with_date_shift(
        GCLOUD_PROJECT,
        input_csv_file=CSV_FILE,
        output_csv_file=output_filepath,
        lower_bound_days=DATE_SHIFTED_AMOUNT,
        upper_bound_days=DATE_SHIFTED_AMOUNT,
        date_fields=DATE_FIELDS,
    )

    out, _ = capsys.readouterr()

    assert "Successful" in out


def test_deidentify_with_date_shift_using_context_field(
    tempdir: TextIO, capsys: pytest.CaptureFixture
) -> None:
    output_filepath = os.path.join(tempdir, "dates-shifted.csv")

    deid.deidentify_with_date_shift(
        GCLOUD_PROJECT,
        input_csv_file=CSV_FILE,
        output_csv_file=output_filepath,
        lower_bound_days=DATE_SHIFTED_AMOUNT,
        upper_bound_days=DATE_SHIFTED_AMOUNT,
        date_fields=DATE_FIELDS,
        context_field_id=CSV_CONTEXT_FIELD,
        wrapped_key=WRAPPED_KEY,
        key_name=KEY_NAME,
    )

    out, _ = capsys.readouterr()

    assert "Successful" in out
