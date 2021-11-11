# Copyright 2020 Google Inc.
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

import custom_infotype

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_inspect_string_with_exclusion_dict(capsys):
    custom_infotype.inspect_string_with_exclusion_dict(
        GCLOUD_PROJECT, "gary@example.com, example@example.com", ["example@example.com"]
    )

    out, _ = capsys.readouterr()
    assert "example@example.com" not in out
    assert "gary@example.com" in out


def test_inspect_string_with_exclusion_regex(capsys):
    custom_infotype.inspect_string_with_exclusion_regex(
        GCLOUD_PROJECT, "alice@example.com, ironman@avengers.net", ".+@example.com"
    )

    out, _ = capsys.readouterr()
    assert "alice" not in out
    assert "ironman" in out


def test_inspect_string_with_exclusion_dict_substring(capsys):
    custom_infotype.inspect_string_with_exclusion_dict_substring(
        GCLOUD_PROJECT, "bob@example.com TEST@example.com TEST.com", ["TEST"]
    )

    out, _ = capsys.readouterr()
    assert "TEST@example.com" not in out
    assert "TEST.com" not in out
    assert "bob@example.com" in out


def test_inspect_string_custom_excluding_substring(capsys):
    custom_infotype.inspect_string_custom_excluding_substring(
        GCLOUD_PROJECT, "Danger, Jimmy | Wayne, Bruce", ["Jimmy"]
    )

    out, _ = capsys.readouterr()
    assert "Wayne, Bruce" in out
    assert "Danger, Jimmy" not in out


def test_inspect_string_custom_omit_overlap(capsys):
    custom_infotype.inspect_string_custom_omit_overlap(
        GCLOUD_PROJECT, "Larry Page and John Doe"
    )

    out, _ = capsys.readouterr()
    assert "Larry Page" not in out
    assert "John Doe" in out


def test_omit_name_if_also_email(capsys):
    custom_infotype.omit_name_if_also_email(GCLOUD_PROJECT, "alice@example.com")

    # Ensure we found only EMAIL_ADDRESS, and not PERSON_NAME.
    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out
    assert "Info type: PERSON_NAME" not in out


def test_inspect_string_without_overlap(capsys):
    custom_infotype.inspect_string_without_overlap(
        GCLOUD_PROJECT, "example.com is a domain, james@example.org is an email."
    )

    out, _ = capsys.readouterr()
    assert "example.com" in out
    assert "example.org" not in out


def test_inspect_with_person_name_w_custom_hotword(capsys):
    custom_infotype.inspect_with_person_name_w_custom_hotword(
        GCLOUD_PROJECT, "patient's name is John Doe.", "patient"
    )

    out, _ = capsys.readouterr()
    assert "Info type: PERSON_NAME" in out
    assert "Likelihood: 5" in out


def test_inspect_string_multiple_rules_patient(capsys):
    custom_infotype.inspect_string_multiple_rules(
        GCLOUD_PROJECT, "patient name: Jane Doe"
    )

    out, _ = capsys.readouterr()
    assert "Likelihood: 4" in out


def test_inspect_string_multiple_rules_doctor(capsys):
    custom_infotype.inspect_string_multiple_rules(GCLOUD_PROJECT, "doctor: Jane Doe")

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_string_multiple_rules_quasimodo(capsys):
    custom_infotype.inspect_string_multiple_rules(
        GCLOUD_PROJECT, "patient name: quasimodo"
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_string_multiple_rules_redacted(capsys):
    custom_infotype.inspect_string_multiple_rules(
        GCLOUD_PROJECT, "name of patient: REDACTED"
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_with_medical_record_number_custom_regex_detector(capsys):
    custom_infotype.inspect_with_medical_record_number_custom_regex_detector(
        GCLOUD_PROJECT, "Patients MRN 444-5-22222"
    )

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out


def test_inspect_with_medical_record_number_w_custom_hotwords_no_hotwords(capsys):
    custom_infotype.inspect_with_medical_record_number_w_custom_hotwords(
        GCLOUD_PROJECT, "just a number 444-5-22222"
    )

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out
    assert "Likelihood: 3" in out


def test_inspect_with_medical_record_number_w_custom_hotwords_has_hotwords(capsys):
    custom_infotype.inspect_with_medical_record_number_w_custom_hotwords(
        GCLOUD_PROJECT, "Patients MRN 444-5-22222"
    )

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out
    assert "Likelihood: 5" in out
