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

import inspect_image_listed_infotypes as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources")


def test_inspect_image_file_listed_infotypes(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_image_file_listed_infotypes(
        GCLOUD_PROJECT,
        test_filepath,
        ["EMAIL_ADDRESS"],
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out
