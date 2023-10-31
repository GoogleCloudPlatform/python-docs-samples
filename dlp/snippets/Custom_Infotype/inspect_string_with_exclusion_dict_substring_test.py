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

import inspect_string_with_exclusion_dict_substring as custom_infotype

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


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
