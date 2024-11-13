# Copyright 2023 Google LLC
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

import os
import re
from uuid import uuid4

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

import pytest

import transcribe_feature_in_recognizer

_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def delete_recognizer(recognizer_id: str) -> None:
    client = SpeechClient()
    request = cloud_speech.DeleteRecognizerRequest(
        name=f"projects/{PROJECT_ID}/locations/global/recognizers/{recognizer_id}"
    )
    client.delete_recognizer(request=request)


def test_transcribe_feature_in_recognizer(
    capsys: pytest.CaptureFixture, request: pytest.FixtureRequest
) -> None:
    recognizer_id = "recognizer-" + str(uuid4())

    def cleanup() -> None:
        delete_recognizer(recognizer_id)

    request.addfinalizer(cleanup)

    response_with_new_recognizer = (
        transcribe_feature_in_recognizer.transcribe_feature_in_recognizer(
            os.path.join(_RESOURCES, "audio.wav"), recognizer_id
        )
    )
    # Call function one more time to test work with the existing recognizer
    response_with_existing_recognizer = (
        transcribe_feature_in_recognizer.transcribe_feature_in_recognizer(
            os.path.join(_RESOURCES, "fair.wav"), recognizer_id
        )
    )
    out, _ = capsys.readouterr()
    assert re.search(
        r"How old is the Brooklyn Bridge?",
        response_with_new_recognizer.results[0].alternatives[0].transcript,
        re.DOTALL | re.I,
    )
    assert re.search(
        r"is fair",
        response_with_existing_recognizer.results[0].alternatives[0].transcript,
        re.DOTALL | re.I,
    )
