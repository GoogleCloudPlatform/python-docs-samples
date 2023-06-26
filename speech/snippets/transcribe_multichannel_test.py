# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.api_core.retry import Retry
import pytest

from transcribe_multichannel import (
    transcribe_file_with_multichannel,
    transcribe_gcs_with_multichannel,
)

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
def test_transcribe_multichannel_file(capsys: pytest.CaptureFixture) -> None:
    result = transcribe_file_with_multichannel(os.path.join(RESOURCES, "multi.wav"))
    out, err = capsys.readouterr()

    assert "how are you doing" in out
    assert result is not None


@Retry()
def test_transcribe_multichannel_gcs(capsys: pytest.CaptureFixture) -> None:
    result = transcribe_gcs_with_multichannel(
        "gs://cloud-samples-data/speech/multi.wav"
    )
    out, err = capsys.readouterr()

    assert "how are you doing" in out
    assert result is not None
