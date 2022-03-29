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

import logging

import pytest

from .. import download_public_data_sandbox

pytest.importorskip("google.cloud.bigquery_storage_v1")


def test_download_public_data_sandbox(
    caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture[str]
) -> None:
    # Enable debug-level logging to verify the BigQuery Storage API is used.
    caplog.set_level(logging.DEBUG)

    download_public_data_sandbox.download_public_data_sandbox()
    out, err = capsys.readouterr()
    assert "year" in out
    assert "gender" in out
    assert "name" in out

    assert any(
        # An anonymous table is used because this sample reads from query results.
        ("Started reading table" in message and "BQ Storage API session" in message)
        for message in caplog.messages
    )
