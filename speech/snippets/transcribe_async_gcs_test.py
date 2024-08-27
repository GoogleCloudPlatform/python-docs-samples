# Copyright 2021 Google LLC
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

import re

from google.api_core.retry import Retry

import transcribe_async_gcs
import transcribe_diarization_gcs_beta
import transcribe_word_level_confidence_gcs_beta

BUCKET = "cloud-samples-data"
GCS_AUDIO_PATH = "gs://" + BUCKET + "/speech/brooklyn_bridge.flac"
GCS_DIARIZATION_AUDIO_PATH = "gs://" + BUCKET + "/speech/commercial_mono.wav"


@Retry()
def test_transcribe_gcs() -> None:
    transcript = transcribe_async_gcs.transcribe_gcs(GCS_AUDIO_PATH)
    assert re.search(r"how old is the Brooklyn Bridge", transcript, re.DOTALL | re.I)


def test_transcribe_diarization_gcs_beta() -> None:
    is_completed = transcribe_diarization_gcs_beta.transcribe_diarization_gcs_beta(
        GCS_DIARIZATION_AUDIO_PATH
    )
    assert is_completed


def test_transcribe_word_level_confidence_gcs_beta() -> None:
    transcript = transcribe_word_level_confidence_gcs_beta.transcribe_file_with_word_level_confidence(
        GCS_AUDIO_PATH
    )
    assert re.search("Transcript: how old is the Brooklyn Bridge", transcript)
    assert re.search("First Word and Confidence: \\(how", transcript)
