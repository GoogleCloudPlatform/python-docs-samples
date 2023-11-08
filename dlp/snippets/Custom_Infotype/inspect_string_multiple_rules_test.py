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

import inspect_string_multiple_rules as custom_infotype

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


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
