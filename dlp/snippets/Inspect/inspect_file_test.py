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

import inspect_file as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources")


def test_inspect_file(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.txt")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out


def test_inspect_file_with_custom_info_types(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.txt")
    dictionaries = ["gary@somedomain.com"]
    regexes = ["\\(\\d{3}\\) \\d{3}-\\d{4}"]

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        [],
        custom_dictionaries=dictionaries,
        custom_regexes=regexes,
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: CUSTOM_DICTIONARY_0" in out
    assert "Info type: CUSTOM_REGEX_0" in out


def test_inspect_file_no_results(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "harmless.txt")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_image_file(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
