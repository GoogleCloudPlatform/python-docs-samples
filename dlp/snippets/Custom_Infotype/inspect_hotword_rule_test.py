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

import inspect_hotword_rule as custom_infotype

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_inspect_with_medical_record_number_w_custom_hotwords_no_hotwords(
    capsys: pytest.LogCaptureFixture,
) -> None:
    custom_infotype.inspect_data_w_custom_hotwords(
        GCLOUD_PROJECT, "just a number 444-5-22222"
    )

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out
    assert "Likelihood: 3" in out


def test_inspect_with_medical_record_number_w_custom_hotwords_has_hotwords(
    capsys: pytest.LogCaptureFixture,
) -> None:
    custom_infotype.inspect_data_w_custom_hotwords(
        GCLOUD_PROJECT, "Patients MRN 444-5-22222"
    )

    out, _ = capsys.readouterr()
    assert "Info type: C_MRN" in out
    assert "Likelihood: 5" in out
