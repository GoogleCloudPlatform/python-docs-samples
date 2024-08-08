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

import transcribe_word_level_confidence_gcs_beta


@Retry()
def test_transcribe_file_with_multilanguage_gcs() -> None:
    audio = "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
    response = transcribe_word_level_confidence_gcs_beta.transcribe_file_with_word_level_confidence(
        audio
    )
    assert "how old is the Brooklyn Bridge" in response
    assert "Confidence: (how, 0" in response
