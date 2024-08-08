# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.api_core.retry import Retry

import pytest

import transcribe_diarization_gcs_beta

_TEST_AUDIO_URI = "gs://cloud-samples-data/speech/commercial_mono.wav"


@Retry()
def test_transcribe_chirp(capsys: pytest.CaptureFixture) -> None:
    response = transcribe_diarization_gcs_beta.transcribe_diarization_gcs_beta(
        _TEST_AUDIO_URI
    )
    out, _ = capsys.readouterr()
    assert "speaker_tag: 1" in out
    assert "speaker_tag: 2" in out
    assert "Brooke" in out
    assert response
