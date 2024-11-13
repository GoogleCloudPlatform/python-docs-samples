# Copyright 2018 Google LLC
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

import transcribe_enhanced_model

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
def test_transcribe_file_with_enhanced_model(capsys: pytest.CaptureFixture) -> None:
    result = transcribe_enhanced_model.transcribe_file_with_enhanced_model(
        "resources/commercial_mono.wav"
    )
    out, _ = capsys.readouterr()

    assert result is not None
    assert "Chrome" in out
    assert "First alternative" in out
    assert "result 7" in out
