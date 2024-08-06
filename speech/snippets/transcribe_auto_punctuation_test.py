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

import transcribe_auto_punctuation

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@Retry()
def test_transcribe_file_with_auto_punctuation(capsys: pytest.CaptureFixture) -> None:
    result = transcribe_auto_punctuation.transcribe_file_with_auto_punctuation(
        os.path.join(RESOURCES, "commercial_mono.wav")
    )
    out, _ = capsys.readouterr()

    assert "First alternative of result " in out
    assert result is not None
