# Copyright 2022 Google LLC
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
import re

from flaky import flaky

from google.cloud.speech_v2.types import cloud_speech
import pytest

import transcribe_streaming_voice_activity_timeouts

_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@flaky(max_runs=3, min_passes=1)
def test_transcribe_silence_padding_timeouts(capsys: pytest.CaptureFixture) -> None:
    responses = transcribe_streaming_voice_activity_timeouts.transcribe_streaming_voice_activity_timeouts(
        1,
        5,
        os.path.join(_RESOURCES, "audio_silence_padding.wav"),
    )

    # This assert doesn't seem deterministic. We should consider removing or changing.
    assert len(responses) == 0


@flaky(max_runs=3, min_passes=1)
def test_transcribe_streaming_voice_activity_timeouts(
    capsys: pytest.CaptureFixture,
) -> None:
    responses = transcribe_streaming_voice_activity_timeouts.transcribe_streaming_voice_activity_timeouts(
        5,
        1,
        os.path.join(_RESOURCES, "audio_silence_padding.wav"),
    )
    transcript = ""
    for response in responses:
        for result in response.results:
            transcript += result.alternatives[0].transcript

    assert (
        responses[0].speech_event_type
        == cloud_speech.StreamingRecognizeResponse.SpeechEventType.SPEECH_ACTIVITY_BEGIN
    )

    assert (
        responses[1].speech_event_type
        == cloud_speech.StreamingRecognizeResponse.SpeechEventType.SPEECH_ACTIVITY_END
    )

    assert re.search(
        r"how old is the Brooklyn Bridge",
        transcript,
        re.DOTALL | re.I,
    )
