# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from .. import download_public_data

pytest.importorskip("google.cloud.bigquery_storage_v1")


def test_download_public_data(capsys: pytest.CaptureFixture[str]) -> None:
    download_public_data.download_public_data()
    out, _ = capsys.readouterr()
    assert "year" in out
    assert "gender" in out
    assert "name" in out
