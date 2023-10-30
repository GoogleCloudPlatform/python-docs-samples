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

import pytest

import custom_infotype

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_inspect_string_with_exclusion_regex(capsys: pytest.LogCaptureFixture) -> None:
    custom_infotype.inspect_string_with_exclusion_regex(
        GCLOUD_PROJECT, "alice@example.com, ironman@avengers.net", ".+@example.com"
    )

    out, _ = capsys.readouterr()
    assert "alice" not in out
    assert "ironman" in out


def test_inspect_string_with_exclusion_dict_substring(
    capsys: pytest.LogCaptureFixture,
) -> None:
    custom_infotype.inspect_string_with_exclusion_dict_substring(
        GCLOUD_PROJECT, "bob@example.com TEST@example.com TEST.com", ["TEST"]
    )

    out, _ = capsys.readouterr()
    assert "TEST@example.com" not in out
    assert "TEST.com" not in out
    assert "bob@example.com" in out


def test_inspect_string_omit_overlap(capsys: pytest.LogCaptureFixture) -> None:
    custom_infotype.inspect_string_omit_overlap(GCLOUD_PROJECT, "alice@example.com")

    # Ensure we found only EMAIL_ADDRESS, and not PERSON_NAME.
    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out
    assert "Info type: PERSON_NAME" not in out


def test_inspect_string_without_overlap(capsys: pytest.LogCaptureFixture) -> None:
    custom_infotype.inspect_string_without_overlap(
        GCLOUD_PROJECT, "example.com is a domain, james@example.org is an email."
    )

    out, _ = capsys.readouterr()
    assert "example.com" in out
    assert "example.org" not in out


def test_inspect_string_multiple_rules_patient(
    capsys: pytest.LogCaptureFixture,
) -> None:
    custom_infotype.inspect_string_multiple_rules(
        GCLOUD_PROJECT, "patient name: Jane Doe"
    )

    out, _ = capsys.readouterr()
    assert "Likelihood: 4" in out


def test_inspect_string_multiple_rules_doctor(capsys: pytest.LogCaptureFixture) -> None:
    custom_infotype.inspect_string_multiple_rules(GCLOUD_PROJECT, "doctor: Jane Doe")

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_string_multiple_rules_quasimodo(
    capsys: pytest.LogCaptureFixture,
) -> None:
    custom_infotype.inspect_string_multiple_rules(
        GCLOUD_PROJECT, "patient name: quasimodo"
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_string_multiple_rules_redacted(
    capsys: pytest.LogCaptureFixture,
) -> None:
    custom_infotype.inspect_string_multiple_rules(
        GCLOUD_PROJECT, "name of patient: REDACTED"
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out
