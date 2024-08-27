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

import pytest

import redact_image as redact

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources")


@pytest.fixture(scope="module")
def tempdir() -> Iterator[TextIO]:
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


def test_redact_image_file(tempdir: TextIO, capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")
    output_filepath = os.path.join(tempdir, "redacted.png")

    redact.redact_image(
        GCLOUD_PROJECT,
        test_filepath,
        output_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
    )

    out, _ = capsys.readouterr()
    assert output_filepath in out
