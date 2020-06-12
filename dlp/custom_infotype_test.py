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

GCLOUD_PROJECT = os.getenv("GCLOUD_PROJECT")


def test_omit_name_if_also_email(capsys):
    info_types = custom_infotype.omit_name_if_also_email(
        GCLOUD_PROJECT, "alice@example.com")

    # Ensure we found only EMAIL_ADDRESS, and not PERSON_NAME.
    assert len(info_types) == 1
    assert info_types[0] == "EMAIL_ADDRESS"


def test_inspect_with_person_name_w_custom_hotword(capsys):
    custom_infotype.inspect_with_person_name_w_custom_hotword(
        GCLOUD_PROJECT, "patient's name is John Doe.", "patient")

    out, _ = capsys.readouterr()
    assert "Info type: PERSON_NAME" in out
    assert "Likelihood: 5" in out


def test_inspect_with_medical_record_number_custom_regex_detector(capsys):
    custom_infotype.inspect_with_medical_record_number_custom_regex_detector(
        GCLOUD_PROJECT, "Patients MRN 444-5-22222")

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out


def test_inspect_with_medical_record_number_w_custom_hotwords_no_hotwords(
        capsys):
    custom_infotype.inspect_with_medical_record_number_w_custom_hotwords(
        GCLOUD_PROJECT, "just a number 444-5-22222")

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out
    assert "Likelihood: 3" in out


def test_inspect_with_medical_record_number_w_custom_hotwords_has_hotwords(
        capsys):
    custom_infotype.inspect_with_medical_record_number_w_custom_hotwords(
        GCLOUD_PROJECT, "Patients MRN 444-5-22222")

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out
    assert "Likelihood: 5" in out
