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

import inspect_augment_infotypes as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_inspect_string_augment_infotype(capsys: pytest.CaptureFixture) -> None:
    inspect_content.inspect_string_augment_infotype(
        GCLOUD_PROJECT,
        "The patient's name is Quasimodo",
        "PERSON_NAME",
        ["quasimodo"],
    )
    out, _ = capsys.readouterr()
    assert "Quote: Quasimodo" in out
    assert "Info type: PERSON_NAME" in out
