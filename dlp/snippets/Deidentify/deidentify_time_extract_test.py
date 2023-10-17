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

import deidentify_time_extract as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
CSV_FILE = os.path.join(os.path.dirname(__file__), "../resources/dates.csv")
DATE_FIELDS = ["birth_date", "register_date"]


@pytest.fixture(scope="module")
def tempdir() -> Iterator[TextIO]:
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


def test_deidentify_with_time_extract(
    tempdir: TextIO, capsys: pytest.CaptureFixture
) -> None:
    output_filepath = os.path.join(str(tempdir), "year-extracted.csv")

    deid.deidentify_with_time_extract(
        GCLOUD_PROJECT,
        input_csv_file=CSV_FILE,
        output_csv_file=output_filepath,
        date_fields=DATE_FIELDS,
    )

    out, _ = capsys.readouterr()

    assert "Successful" in out
