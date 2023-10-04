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

import deidentify_table_primitive_bucketing as deid

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_deidentify_table_primitive_bucketing(capsys: pytest.CaptureFixture) -> None:
    deid.deidentify_table_primitive_bucketing(
        GCLOUD_PROJECT,
    )

    out, _ = capsys.readouterr()
    assert 'string_value: "High"' in out
    assert 'string_value: "Low"' in out
